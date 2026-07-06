"""Global template context for SEO and site metadata."""
from django.conf import settings

from apps.landing.models import SiteContact
from apps.landing.services import get_site_links


def site_settings(request):
    contact = SiteContact.objects.filter(pk=1).first()

    return {
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
        'site_description': settings.SITE_DESCRIPTION,
        'site_keywords': settings.SITE_KEYWORDS,
        'site_phone': contact.phone if contact else settings.SITE_PHONE,
        'site_email': contact.email if contact else settings.SITE_EMAIL,
        'site_address': contact.address if contact else settings.SITE_ADDRESS,
        'site_vk_url': contact.vk_url if contact else settings.SITE_VK_URL,
        'site_vk_label': contact.vk_label if contact else 'darovanie34',
        'site_legacy_url': contact.legacy_url if contact and contact.legacy_url else settings.SITE_LEGACY_URL,
        'site_contact': contact,
        'default_theme': settings.DEFAULT_THEME,
        'nav_links': get_site_links('nav'),
        'footer_school_links': get_site_links('footer_school'),
        'footer_doc_links': get_site_links('footer_doc'),
        'footer_tagline': contact.footer_tagline if contact else (
            'Образовательный центр, где учеба в радость. '
            'Индивидуальный подход и комфортная среда для каждого ребенка.'
        ),
    }
