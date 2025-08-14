from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    
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
    
    # Task Actions
    path('tasks/<uuid:pk>/comment/', views.add_comment, name='add_comment'),
    path('tasks/<uuid:pk>/attachment/', views.add_attachment, name='add_attachment'),
    path('tasks/<uuid:pk>/status/', views.task_status_update, name='task_status_update'),
    
    # API Endpoints
    path('api/project/<uuid:pk>/progress/', views.project_progress_data, name='project_progress_data'),
    
    # User Management
    path('users/', views.user_list, name='user_list'),
    path('users/<uuid:pk>/', views.user_detail, name='user_detail'),
]


