from django import forms
from django.contrib.auth import get_user_model
from .models import Project, Task, TaskComment, TaskAttachment, ProjectMember

User = get_user_model()

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'status', 'priority', 'start_date', 'end_date', 'budget', 'members']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Project Description'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Budget Amount'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter members based on user role
        if 'instance' in kwargs and kwargs['instance']:
            project = kwargs['instance']
            if hasattr(project, 'owner'):
                # Only show users that the project owner can add
                self.fields['members'].queryset = User.objects.filter(is_active=True)
        else:
            self.fields['members'].queryset = User.objects.filter(is_active=True)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'status', 'priority', 'due_date', 'estimated_hours', 'actual_hours', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Task Description'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estimated_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Estimated Hours'}),
            'actual_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Actual Hours'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags (comma separated)'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filter projects based on user access
            if user.role == 'admin':
                self.fields['project'].queryset = Project.objects.all()
            else:
                self.fields['project'].queryset = Project.objects.filter(members=user)
            
            # Filter assignable users based on project members
            if 'instance' in kwargs and kwargs['instance']:
                task = kwargs['instance']
                if task.project:
                    self.fields['assigned_to'].queryset = task.project.members.all()
            else:
                self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            # Convert comma-separated tags to list
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            return tag_list
        return []

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }

class TaskAttachmentForm(forms.ModelForm):
    class Meta:
        model = TaskAttachment
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 10MB.")
            
            # Check file type
            allowed_types = [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'image/jpeg',
                'image/png',
                'image/gif',
                'text/plain',
                'application/zip',
                'application/x-rar-compressed'
            ]
            
            if file.content_type not in allowed_types:
                raise forms.ValidationError("File type not allowed.")
        
        return file

class ProjectMemberForm(forms.ModelForm):
    class Meta:
        model = ProjectMember
        fields = ['user', 'role']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        
        if project:
            # Exclude users already in the project
            existing_members = project.members.all()
            self.fields['user'].queryset = User.objects.filter(is_active=True).exclude(id__in=existing_members.values_list('id', flat=True))

class UserSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search users...'
        })
    )
    role = forms.ChoiceField(
        choices=[('', 'All Roles')] + User.ROLE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class TaskFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Task.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    priority = forms.ChoiceField(
        choices=[('', 'All Priorities')] + Task.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.none(),
        required=False,
        empty_label="All Projects",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        empty_label="All Users",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            if user.role == 'admin':
                self.fields['project'].queryset = Project.objects.all()
                self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)
            else:
                self.fields['project'].queryset = Project.objects.filter(members=user)
                self.fields['assigned_to'].queryset = user.projects.all().distinct()

class ProjectFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Project.status_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    priority = forms.ChoiceField(
        choices=[('', 'All Priorities')] + Project.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    owner = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        empty_label="All Owners",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.role == 'admin':
            self.fields['owner'].queryset = User.objects.filter(is_active=True)


