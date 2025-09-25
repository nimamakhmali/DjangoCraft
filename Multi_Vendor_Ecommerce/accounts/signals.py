from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import CustomUser, VendorProfile, CustomerProfile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create user profiles when a user is created.
    
    Args:
        sender: The model class (CustomUser)
        instance: The actual instance being saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    if created:
        # Create appropriate profile based on user role
        if instance.role == CustomUser.UserRole.VENDOR:
            VendorProfile.objects.create(
                user=instance,
                business_email=instance.email,
                business_phone=instance.phone_number or ''
            )
        elif instance.role == CustomUser.UserRole.CUSTOMER:
            CustomerProfile.objects.create(user=instance)
        
        # Log the profile creation
        print(f"Created {instance.role} profile for user: {instance.username}")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to automatically save user profiles when a user is updated.
    
    Args:
        sender: The model class (CustomUser)
        instance: The actual instance being saved
        **kwargs: Additional keyword arguments
    """
    try:
        if instance.role == CustomUser.UserRole.VENDOR:
            if hasattr(instance, 'vendor_profile'):
                instance.vendor_profile.save()
        elif instance.role == CustomUser.UserRole.CUSTOMER:
            if hasattr(instance, 'customer_profile'):
                instance.customer_profile.save()
    except Exception as e:
        # Log any errors that occur during profile saving
        print(f"Error saving profile for user {instance.username}: {e}")


@receiver(post_save, sender=VendorProfile)
def handle_vendor_approval(sender, instance, **kwargs):
    """
    Signal to handle vendor approval status changes.
    
    Args:
        sender: The model class (VendorProfile)
        instance: The actual instance being saved
        **kwargs: Additional keyword arguments
    """
    if instance.is_approved and not instance.approval_date:
        # Set approval date when vendor is first approved
        instance.approval_date = timezone.now()
        instance.save(update_fields=['approval_date'])
        
        # Update the user's vendor status
        if instance.user:
            instance.user.is_active_vendor = True
            instance.user.save(update_fields=['is_active_vendor'])
            
        print(f"Vendor {instance.store_name} approved on {instance.approval_date}")
    
    elif not instance.is_approved and instance.approval_date:
        # Clear approval date when vendor is disapproved
        instance.approval_date = None
        instance.save(update_fields=['approval_date'])
        
        # Update the user's vendor status
        if instance.user:
            instance.user.is_active_vendor = False
            instance.user.save(update_fields=['is_active_vendor'])
            
        print(f"Vendor {instance.store_name} disapproved")


@receiver(post_save, sender=CustomUser)
def handle_role_change(sender, instance, **kwargs):
    """
    Signal to handle user role changes.
    This ensures that users have the correct profile type.
    
    Args:
        sender: The model class (CustomUser)
        instance: The actual instance being saved
        **kwargs: Additional keyword arguments
    """
    # Check if this is an update (not creation)
    if not kwargs.get('created', False):
        # Get the old instance from database to compare roles
        try:
            old_instance = CustomUser.objects.get(pk=instance.pk)
            if old_instance.role != instance.role:
                # Role has changed, handle profile migration
                handle_role_migration(old_instance, instance)
        except CustomUser.DoesNotExist:
            # User doesn't exist yet, this is a creation
            pass


def handle_role_migration(old_instance, new_instance):
    """
    Handle migration of user profiles when role changes.
    
    Args:
        old_instance: The user instance before the change
        new_instance: The user instance after the change
    """
    try:
        # Remove old profile
        if old_instance.role == CustomUser.UserRole.VENDOR:
            if hasattr(old_instance, 'vendor_profile'):
                old_instance.vendor_profile.delete()
        elif old_instance.role == CustomUser.UserRole.CUSTOMER:
            if hasattr(old_instance, 'customer_profile'):
                old_instance.customer_profile.delete()
        
        # Create new profile
        if new_instance.role == CustomUser.UserRole.VENDOR:
            VendorProfile.objects.create(
                user=new_instance,
                business_email=new_instance.email,
                business_phone=new_instance.phone_number or ''
            )
        elif new_instance.role == CustomUser.UserRole.CUSTOMER:
            CustomerProfile.objects.create(user=new_instance)
        
        print(f"Migrated user {new_instance.username} from {old_instance.role} to {new_instance.role}")
        
    except Exception as e:
        print(f"Error during role migration for user {new_instance.username}: {e}")
