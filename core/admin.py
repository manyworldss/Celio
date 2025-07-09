from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import EarlyAccessSignup

@admin.register(EarlyAccessSignup)
class EarlyAccessSignupAdmin(admin.ModelAdmin):
    """Secure admin interface for early access signups"""
    list_display = [
        'email', 
        'display_name', 
        'wants_updates', 
        'is_verified',
        'created_at_formatted',
        'days_since_signup'
    ]
    list_filter = [
        'wants_updates', 
        'is_verified', 
        'created_at'
    ]
    search_fields = ['email', 'name']
    readonly_fields = [
        'created_at', 
        'ip_address', 
        'user_agent',
        'days_since_signup'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('email', 'name')
        }),
        ('Preferences', {
            'fields': ('wants_updates', 'is_verified')
        }),
        ('Security & Tracking', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'days_since_signup'),
            'classes': ('collapse',)
        })
    )
    
    def created_at_formatted(self, obj):
        """Format creation date nicely"""
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_formatted.short_description = 'Signed Up'
    created_at_formatted.admin_order_field = 'created_at'
    
    def days_since_signup(self, obj):
        """Calculate days since signup"""
        delta = timezone.now() - obj.created_at
        return f"{delta.days} days ago"
    days_since_signup.short_description = 'Time Since Signup'
    
    def get_queryset(self, request):
        """Optimize queryset for admin"""
        return super().get_queryset(request).select_related()
    
    # Security: Only allow superusers to delete signups
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    # Export functionality
    actions = ['export_emails']
    
    def export_emails(self, request, queryset):
        """Export selected emails as CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="early_access_emails.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Name', 'Wants Updates', 'Verified', 'Signup Date'])
        
        for signup in queryset:
            writer.writerow([
                signup.email,
                signup.name,
                signup.wants_updates,
                signup.is_verified,
                signup.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        
        return response
    export_emails.short_description = "Export selected emails as CSV"
