
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import json

from .models import Project, Task, Team, User, ProjectMember, TaskComment, TaskAttachment, TeamMember
from .forms import ProjectForm, TaskForm, TaskCommentForm, TaskAttachmentForm, ProjectMemberForm, UserSearchForm, TaskFilterForm, ProjectFilterForm, CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm



User = get_user_model()

@login_required
def dashboard(request) -> render:
    user = request.user

    if user.role == 'admin':
        projects = Project.objects.all()
        tasks = Task.objects.all()
    else:
        projects = Project.objects.filter(members=user)
        tasks = Task.objects.filter(
            Q(project__members=user) | Q(assigned_to=user)
        )  
 # Statistics
    total_projects     = projects.count()
    active_projects    = projects.filter(status='active').count()      
    completed_projects = projects.filter(status='completed').count()
    total_tasks        = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    overdue_tasks = tasks.filter(
        due_date__lt=timezone.now(),
        status__in=['todo', 'in_progress', 'review']
    ).count()    
  # Recent activities
    recent_tasks = tasks.order_by('-created_at')[:5]
    recent_projects = projects.order_by('-created_at')[:5]
    
    # Tasks by status
    tasks_by_status = tasks.values('status').annotate(count=Count('id'))
    
    context = {
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'recent_tasks': recent_tasks,
        'recent_projects': recent_projects,
        'tasks_by_status': tasks_by_status,
    }
    
    return render(request, 'core/dashboard.html', context)



# Project Views
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'core/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Project.objects.all()
        return Project.objects.filter(members=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', '')
        context['priority_filter'] = self.request.GET.get('priority', '')
        
        # Apply filters
        queryset = context['projects']
        if context['status_filter']:
            queryset = queryset.filter(status=context['status_filter'])
        if context['priority_filter']:
            queryset = queryset.filter(priority=context['priority_filter'])
        
        context['projects'] = queryset
        return context
 

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Check if user has access to this project
        if not self.request.user.role == 'admin' and self.request.user not in project.members.all():
            messages.error(self.request, "You don't have access to this project.")
            return redirect('project_list')
        
        # Get project tasks
        tasks = project.tasks.all()
        context['tasks'] = tasks
        context['task_count'] = tasks.count()
        context['completed_tasks'] = tasks.filter(status='completed').count()
        context['overdue_tasks'] = tasks.filter(
            due_date__lt=timezone.now(),
            status__in=['todo', 'in_progress', 'review']
        ).count()
        
        # Get project members
        context['members'] = project.projectmember_set.all()
        
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/project_form.html'
    success_url = reverse_lazy('project_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Project created successfully!')
        return response


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/project_form.html'
    
    def test_func(self):
        project = self.get_object()
        return (
            self.request.user.role == 'admin' or
            project.owner == self.request.user or
            project.projectmember_set.filter(user=self.request.user, role__in=['owner', 'manager']).exists()
        )
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Project updated successfully!')
        return response
 

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'core/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')
    
    def test_func(self):
        project = self.get_object()
        return (
            self.request.user.role == 'admin' or
            project.owner == self.request.user
        )
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)



# Task Views
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'core/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 15
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Task.objects.all()
        return Task.objects.filter(
            Q(project__members=user) | Q(assigned_to=user)
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', '')
        context['priority_filter'] = self.request.GET.get('priority', '')
        context['project_filter'] = self.request.GET.get('project', '')
        
        # Apply filters
        queryset = context['tasks']
        if context['status_filter']:
            queryset = queryset.filter(status=context['status_filter'])
        if context['priority_filter']:
            queryset = queryset.filter(priority=context['priority_filter'])
        if context['project_filter']:
            queryset = queryset.filter(project_id=context['project_filter'])
        
        context['tasks'] = queryset
        context['projects'] = Project.objects.filter(members=self.request.user)
        return context
 

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'core/task_detail.html'
    context_object_name = 'task'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        
        # Check access
        if not self.request.user.role == 'admin' and self.request.user not in task.project.members.all():
            messages.error(self.request, "You don't have access to this task.")
            return redirect('task_list')
        
        # Get comments and attachments
        context['comments'] = task.comments.all()
        context['attachments'] = task.attachments.all()
        context['comment_form'] = TaskCommentForm()
        context['attachment_form'] = TaskAttachmentForm()
        
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'core/task_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Task created successfully!')
        return response
    
    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'core/task_form.html'
    
    def test_func(self):
        task = self.get_object()
        return (
            self.request.user.role == 'admin' or
            task.created_by == self.request.user or
            task.assigned_to == self.request.user or
            task.project.owner == self.request.user
        )
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Task updated successfully!')
        return response
    
    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'core/task_confirm_delete.html'
    
    def test_func(self):
        task = self.get_object()
        return (
            self.request.user.role == 'admin' or
            task.created_by == self.request.user or
            task.project.owner == self.request.user
        )
    
    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Task deleted successfully!')
        return super().delete(request, *args, **kwargs)



# comment & Attachment
@login_required
def add_comment(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment.')
    
    return redirect('task_detail', pk=task_id)


@login_required
def add_attachment(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        form = TaskAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.task = task
            attachment.uploaded_by = request.user
            attachment.save()
            messages.success(request, 'Attachment uploaded successfully!')
        else:
            messages.error(request, 'Error uploading attachment.')
    
    return redirect('task_detail', pk=task_id)
 

@login_required
def task_status_update(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            return JsonResponse({'success': True, 'status': new_status})
    
    return JsonResponse({'success': False})


@login_required
def project_progress_data(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    tasks_by_status = project.tasks.values('status').annotate(count=Count('id'))
    
    return JsonResponse({
        'progress': project.progress,
        'tasks_by_status': list(tasks_by_status)
    })


@login_required
def user_list(request):
    if request.user.role != 'admin':
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    users = User.objects.all()
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/user_list.html', {'page_obj': page_obj})


@login_required
def user_detail(request, user_id):
    if request.user.role != 'admin' and request.user.id != user_id:
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    user = get_object_or_404(User, id=user_id)
    assigned_tasks = user.assigned_tasks.all()
    owned_projects = user.owned_projects.all()
    
    context = {
        'user_detail': user,
        'assigned_tasks': assigned_tasks,
        'owned_projects': owned_projects,
    }
    
    return render(request, 'core/user_detail.html', context)


# Authentication Views
def login_view(request):
    """Custom login view"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Handle remember me functionality
                if not remember_me:
                    request.session.set_expiry(0)
                
                messages.success(request, f'Welcome back, {user.full_name}!')
                
                # Redirect to next page or dashboard
                next_url = request.GET.get('next')
                if next_url and next_url != '/':
                    return redirect(next_url)
                return redirect('core:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

def register_view(request):
    """Custom registration view"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            
            # Log the user in after registration
            login(request, user)
            messages.success(request, f'Welcome to DjangoCraft, {user.full_name}! Your account has been created successfully.')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/register.html', {'form': form})

@login_required
def logout_view(request):
    """Custom logout view"""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('core:login')
    
    return render(request, 'core/logout.html')

@login_required
def profile_edit_view(request):
    """User profile edit view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('core:user_detail', pk=request.user.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'core/user_profile_edit.html', {'form': form})



