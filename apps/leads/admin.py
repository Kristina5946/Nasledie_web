from django.contrib import admin

from apps.leads.models import ContactLead


@admin.register(ContactLead)
class ContactLeadAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'phone', 'status', 'source',
        'utm_source', 'utm_campaign', 'created_at',
    )
    list_filter = ('status', 'source', 'utm_source', 'utm_campaign', 'created_at')
    search_fields = ('name', 'phone', 'comment', 'utm_campaign')
    readonly_fields = (
        'referrer', 'landing_page', 'user_agent', 'ip_address',
        'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
        'created_at', 'updated_at',
    )
    date_hierarchy = 'created_at'
