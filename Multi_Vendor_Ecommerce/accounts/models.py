from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Supports both vendors and customers with role-based access.
    """
    
    # User roles
    class UserRole(models.TextChoices):
        CUSTOMER = 'customer', _('Customer')
        VENDOR = 'vendor', _('Vendor')
        ADMIN = 'admin', _('Admin')
    
    # Basic user information
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. Enter a valid email address.')
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        help_text=_('Phone number in international format (e.g., +1234567890)')
    )
    
    # User role and status
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
        help_text=_('User role in the system')
    )
    
    is_verified = models.BooleanField(
        default=False,
        help_text=_('Whether the user has verified their email/phone')
    )
    
    is_active_vendor = models.BooleanField(
        default=False,
        help_text=_('Whether the vendor account is active and approved')
    )
    
    # Profile information
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text=_('User date of birth')
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        help_text=_('User profile picture')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Meta information
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_vendor(self):
        """Check if user is a vendor"""
        return self.role == self.UserRole.VENDOR
    
    @property
    def is_customer(self):
        """Check if user is a customer"""
        return self.role == self.UserRole.CUSTOMER
    
    @property
    def is_admin(self):
        """Check if user is an admin"""
        return self.role == self.UserRole.ADMIN
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name if self.first_name else self.username


class VendorProfile(models.Model):
    """
    Extended profile information for vendors.
    """
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='vendor_profile'
    )
    
    # Store information
    store_name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_('Unique name for the vendor store')
    )
    
    store_description = models.TextField(
        blank=True,
        help_text=_('Description of the vendor store')
    )
    
    store_logo = models.ImageField(
        upload_to='store_logos/',
        null=True,
        blank=True,
        help_text=_('Store logo image')
    )
    
    # Business information
    business_license = models.CharField(
        max_length=50,
        blank=True,
        help_text=_('Business license number')
    )
    
    tax_id = models.CharField(
        max_length=50,
        blank=True,
        help_text=_('Tax identification number')
    )
    
    # Contact information
    business_address = models.TextField(
        help_text=_('Business address')
    )
    
    business_phone = models.CharField(
        max_length=17,
        help_text=_('Business phone number')
    )
    
    business_email = models.EmailField(
        help_text=_('Business email address')
    )
    
    # Social media
    website = models.URLField(
        blank=True,
        help_text=_('Vendor website URL')
    )
    
    facebook = models.URLField(
        blank=True,
        help_text=_('Facebook page URL')
    )
    
    instagram = models.URLField(
        blank=True,
        help_text=_('Instagram profile URL')
    )
    
    # Commission and payment
    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,
        help_text=_('Commission rate percentage (e.g., 10.00 for 10%)')
    )
    
    # Status
    is_approved = models.BooleanField(
        default=False,
        help_text=_('Whether the vendor is approved by admin')
    )
    
    approval_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Date when vendor was approved')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Vendor Profile')
        verbose_name_plural = _('Vendor Profiles')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.store_name} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        """Override save to automatically approve vendor if user is admin"""
        if self.user.is_admin:
            self.is_approved = True
            if not self.approval_date:
                from django.utils import timezone
                self.approval_date = timezone.now()
        super().save(*args, **kwargs)


class CustomerProfile(models.Model):
    """
    Extended profile information for customers.
    """
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )
    
    # Personal information
    bio = models.TextField(
        blank=True,
        help_text=_('Customer bio or description')
    )
    
    # Preferences
    newsletter_subscription = models.BooleanField(
        default=True,
        help_text=_('Whether customer wants to receive newsletters')
    )
    
    marketing_emails = models.BooleanField(
        default=True,
        help_text=_('Whether customer wants to receive marketing emails')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Customer Profile')
        verbose_name_plural = _('Customer Profiles')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - Customer Profile"
