from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Project, ProjectMember, Task, TaskAttachment, 
    TaskComment, Team, TeamMember
)

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'avatar', 'bio', 'date_of_birth')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'avatar', 'bio', 'date_of_birth')}),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'priority', 'start_date', 'end_date', 'progress', 'is_overdue')
    list_filter = ('status', 'priority', 'start_date', 'end_date')
    search_fields = ('title', 'description', 'owner__username')
    ordering = ('-created_at',)
    readonly_fields = ('progress', 'is_overdue', 'created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'owner')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('Dates & Budget', {
            'fields': ('start_date', 'end_date', 'budget')
        }),
        ('Members', {
            'fields': ('members',)
        }),
        ('Metadata', {
            'fields': ('progress', 'is_overdue', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'joined_at', 'is_active')
    list_filter = ('role', 'is_active', 'joined_at')
    search_fields = ('user__username', 'project__title')
    ordering = ('-joined_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'status', 'priority', 'due_date', 'is_overdue')
    list_filter = ('status', 'priority', 'due_date', 'project')
    search_fields = ('title', 'description', 'project__title', 'assigned_to__username')
    ordering = ('-created_at',)
    readonly_fields = ('is_overdue', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'project')
        }),
        ('Assignment & Status', {
            'fields': ('assigned_to', 'status', 'priority')
        }),
        ('Time Tracking', {
            'fields': ('due_date', 'estimated_hours', 'actual_hours')
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
        ('Metadata', {
            'fields': ('is_overdue', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )    


@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'task', 'uploaded_by', 'file_size', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('filename', 'task__title', 'uploaded_by__username')
    ordering = ('-uploaded_at',)
    readonly_fields = ('file_size', 'uploaded_at')



@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'task', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'task__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'member_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description', 'created_by__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'team__name')
    ordering = ('team__name', 'user__username')

