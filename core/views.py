
from ast import Delete
from tokenize import Comment
from winreg import DeleteValue
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from mmd import ProjectDeleteView



User = get_user_model()

@login_required
def dashboard(request):
    pass

# Project Views
class ProjectListView(LoginRequiredMixin, ListView):
    pass 

class ProjectDetailView(LoginRequiredMixin, DetailView):
    pass 

class ProjectCreateView(LoginRequiredMixin, CreateView):
    pass 

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    pass 

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    pass


# Task Views
class TaskListView(LoginRequiredMixin, ListView):
    pass 

class TaskDetailView(LoginRequiredMixin, DetailView):
    pass 

class TaskCreateView(LoginRequiredMixin, CreateView):
    pass 

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    pass

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteValue):
    pass 


# comment & Attachment
@login_required
def add_comment(request, task_id):
    pass 

@login_required
def add_attachment(request, task_id):
    pass 

@login_required
def task_status_update(request, task_id):
    pass 

@login_required
def project_progress_data(request, project_id):
    pass 

@login_required
def user_list(request):
    pass

@login_required
def user_detail(request, user_id):
    pass


