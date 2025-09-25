from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, VendorProfile, CustomerProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser model.
    Extends Django's built-in UserAdmin with custom fields.
    """
    
    # Fields to display in the user list
    list_display = [
        'username', 'email', 'first_name', 'last_name', 
        'role', 'is_verified', 'is_active_vendor', 'is_staff', 'is_active'
    ]
    
    # Fields to filter by
    list_filter = [
        'role', 'is_verified', 'is_active_vendor', 'is_staff', 
        'is_active', 'is_superuser', 'date_joined'
    ]
    
    # Fields to search by
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    
    # Fields to display in the user detail form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email', 'phone_number',
                'date_of_birth', 'profile_picture'
            )
        }),
        (_('Role & Status'), {
            'fields': (
                'role', 'is_verified', 'is_active_vendor',
                'is_active', 'is_staff', 'is_superuser'
            )
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
        (_('User permissions'), {'fields': ('user_permissions',)}),
    )
    
    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'first_name', 'last_name', 'role'
            ),
        }),
    )
    
    # Ordering
    ordering = ['-date_joined']
    
    # Actions
    actions = ['verify_users', 'activate_vendors', 'deactivate_vendors']
    
    def verify_users(self, request, queryset):
        """Mark selected users as verified"""
        updated = queryset.update(is_verified=True)
        self.message_user(
            request, 
            f'{updated} user(s) were successfully marked as verified.'
        )
    verify_users.short_description = "Mark selected users as verified"
    
    def activate_vendors(self, request, queryset):
        """Activate selected vendor accounts"""
        vendors = queryset.filter(role=CustomUser.UserRole.VENDOR)
        updated = vendors.update(is_active_vendor=True)
        self.message_user(
            request, 
            f'{updated} vendor account(s) were successfully activated.'
        )
    activate_vendors.short_description = "Activate selected vendor accounts"
    
    def deactivate_vendors(self, request, queryset):
        """Deactivate selected vendor accounts"""
        vendors = queryset.filter(role=CustomUser.UserRole.VENDOR)
        updated = vendors.update(is_active_vendor=False)
        self.message_user(
            request, 
            f'{updated} vendor account(s) were successfully deactivated.'
        )
    deactivate_vendors.short_description = "Deactivate selected vendor accounts"


@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for VendorProfile model.
    """
    
    # Fields to display in the vendor list
    list_display = [
        'store_name', 'user', 'is_approved', 'commission_rate',
        'business_license', 'created_at'
    ]
    
    # Fields to filter by
    list_filter = [
        'is_approved', 'commission_rate', 'created_at', 'updated_at'
    ]
    
    # Fields to search by
    search_fields = [
        'store_name', 'user__username', 'user__email',
        'business_license', 'tax_id'
    ]
    
    # Fields to display in the vendor detail form
    fieldsets = (
        (_('Store Information'), {
            'fields': (
                'user', 'store_name', 'store_description', 'store_logo'
            )
        }),
        (_('Business Information'), {
            'fields': (
                'business_license', 'tax_id', 'commission_rate'
            )
        }),
        (_('Contact Information'), {
            'fields': (
                'business_address', 'business_phone', 'business_email'
            )
        }),
        (_('Social Media'), {
            'fields': ('website', 'facebook', 'instagram'),
            'classes': ('collapse',)
        }),
        (_('Status'), {
            'fields': ('is_approved', 'approval_date')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at']
    
    # Actions
    actions = ['approve_vendors', 'disapprove_vendors']
    
    def approve_vendors(self, request, queryset):
        """Approve selected vendors"""
        from django.utils import timezone
        updated = queryset.update(
            is_approved=True, 
            approval_date=timezone.now()
        )
        self.message_user(
            request, 
            f'{updated} vendor(s) were successfully approved.'
        )
    approve_vendors.short_description = "Approve selected vendors"
    
    def disapprove_vendors(self, request, queryset):
        """Disapprove selected vendors"""
        updated = queryset.update(
            is_approved=False, 
            approval_date=None
        )
        self.message_user(
            request, 
            f'{updated} vendor(s) were successfully disapproved.'
        )
    disapprove_vendors.short_description = "Disapprove selected vendors"


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for CustomerProfile model.
    """
    
    # Fields to display in the customer list
    list_display = [
        'user', 'newsletter_subscription', 'marketing_emails', 'created_at'
    ]
    
    # Fields to filter by
    list_filter = [
        'newsletter_subscription', 'marketing_emails', 'created_at', 'updated_at'
    ]
    
    # Fields to search by
    search_fields = [
        'user__username', 'user__email', 'user__first_name', 'user__last_name'
    ]
    
    # Fields to display in the customer detail form
    fieldsets = (
        (_('User Information'), {
            'fields': ('user',)
        }),
        (_('Personal Information'), {
            'fields': ('bio',)
        }),
        (_('Preferences'), {
            'fields': ('newsletter_subscription', 'marketing_emails')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at']
    
    # Actions
    actions = ['subscribe_to_newsletter', 'unsubscribe_from_newsletter']
    
    def subscribe_to_newsletter(self, request, queryset):
        """Subscribe selected customers to newsletter"""
        updated = queryset.update(newsletter_subscription=True)
        self.message_user(
            request, 
            f'{updated} customer(s) were successfully subscribed to newsletter.'
        )
    subscribe_to_newsletter.short_description = "Subscribe to newsletter"
    
    def unsubscribe_from_newsletter(self, request, queryset):
        """Unsubscribe selected customers from newsletter"""
        updated = queryset.update(newsletter_subscription=False)
        self.message_user(
            request, 
            f'{updated} customer(s) were successfully unsubscribed from newsletter.'
        )
    unsubscribe_from_newsletter.short_description = "Unsubscribe from newsletter"
