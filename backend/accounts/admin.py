from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from .models import User, JobSeeker, Employer, UserFeedback

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'user_type', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'user_type', 'password1', 'password2'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.user_type == 'admin':
            # Disable fields for admin user
            form.base_fields['username'].disabled = True
            form.base_fields['email'].disabled = True
            form.base_fields['user_type'].disabled = True
        return form

    def has_delete_permission(self, request, obj=None):
        if obj and obj.user_type == 'admin':
            return False
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if change and obj.user_type == 'admin':
            # Only allow password change for admin user
            if not any(field in form.changed_data for field in ['password1', 'password2']):
                raise ValidationError('Only password can be changed for admin user.')
        super().save_model(request, obj, form, change)

@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__email', 'user__username', 'skills')
    list_filter = ('created_at', 'updated_at')

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'industry', 'location')
    search_fields = ('company_name', 'user__email', 'industry')
    list_filter = ('industry', 'created_at')

@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'subject', 'is_resolved', 'created_at')
    list_filter = ('feedback_type', 'is_resolved', 'created_at')
    search_fields = ('user__email', 'subject', 'message')
    readonly_fields = ('created_at',)
