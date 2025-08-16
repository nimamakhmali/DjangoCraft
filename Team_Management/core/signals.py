from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import User, Project, ProjectMember, Task, TaskAttachment

@receiver(post_save, sender=Project)
def create_project_owner_member(sender, instance, created, **kwargs):
    """
    Automatically add project owner as a member with 'owner' role
    """
    if created:
        ProjectMember.objects.get_or_create(
            project=instance,
            user=instance.owner,
            defaults={'role': 'owner'}
        )

@receiver(post_save, sender=Task)
def update_project_progress(sender, instance, **kwargs):
    """
    Update project progress when task status changes
    """
    # This will trigger the progress property calculation
    instance.project.save()

@receiver(post_save, sender=TaskAttachment)
def update_task_attachment_info(sender, instance, created, **kwargs):
    """
    Update file information when attachment is created
    """
    if created and instance.file:
        # Update filename and file size
        instance.filename = instance.file.name.split('/')[-1]
        instance.file_size = instance.file.size
        instance.save(update_fields=['filename', 'file_size'])

@receiver(post_delete, sender=TaskAttachment)
def delete_task_attachment_file(sender, instance, **kwargs):
    """
    Delete the actual file when attachment is deleted
    """
    if instance.file:
        try:
            instance.file.delete(save=False)
        except:
            pass  # File might already be deleted

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create additional user profile information if needed
    """
    if created:
        # You can add additional user setup logic here
        pass
