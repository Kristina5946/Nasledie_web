"""Global template context for SEO and site metadata."""
from django.conf import settings

from apps.landing.data import FOOTER_DOC_LINKS, FOOTER_SCHOOL_LINKS, NAV_LINKS


def site_settings(request):
    return {
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
        'site_description': settings.SITE_DESCRIPTION,
        'site_keywords': settings.SITE_KEYWORDS,
        'site_phone': settings.SITE_PHONE,
        'site_email': settings.SITE_EMAIL,
        'site_address': settings.SITE_ADDRESS,
        'site_vk_url': settings.SITE_VK_URL,
        'site_legacy_url': settings.SITE_LEGACY_URL,
        'default_theme': settings.DEFAULT_THEME,
        'nav_links': NAV_LINKS,
        'footer_school_links': FOOTER_SCHOOL_LINKS,
        'footer_doc_links': FOOTER_DOC_LINKS,
    }
