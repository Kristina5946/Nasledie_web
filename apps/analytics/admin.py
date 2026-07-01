from django.contrib import admin

from apps.analytics.models import PageView


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = (
        'event_type', 'path', 'utm_source', 'utm_campaign',
        'ip_address', 'created_at',
    )
    list_filter = ('event_type', 'utm_source', 'utm_campaign', 'created_at')
    search_fields = ('path', 'utm_campaign', 'referrer')
    readonly_fields = (
        'path', 'event_type', 'session_key',
        'utm_source', 'utm_medium', 'utm_campaign',
        'referrer', 'user_agent', 'ip_address',
        'metadata', 'created_at',
    )
    date_hierarchy = 'created_at'
