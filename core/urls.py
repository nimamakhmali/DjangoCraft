from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Project URLs
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<uuid:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<uuid:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<uuid:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    
    # Task URLs
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<uuid:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<uuid:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<uuid:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    
    # Comment and Attachment URLs
    path('tasks/<uuid:task_id>/comment/', views.add_comment, name='add_comment'),
    path('tasks/<uuid:task_id>/attachment/', views.add_attachment, name='add_attachment'),
    
    # API URLs for AJAX
    path('api/tasks/<uuid:task_id>/status/', views.task_status_update, name='task_status_update'),
    path('api/projects/<uuid:project_id>/progress/', views.project_progress_data, name='project_progress_data'),
    
    # User Management URLs
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
]


