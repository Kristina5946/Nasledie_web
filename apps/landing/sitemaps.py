"""Sitemap for public landing and legal pages."""
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

# Public pages indexed for Yandex/Google
PUBLIC_PAGES = (
    {
        'name': 'landing:index',
        'priority': 1.0,
        'changefreq': 'weekly',
    },
    {
        'name': 'landing:privacy',
        'priority': 0.5,
        'changefreq': 'monthly',
    },
    {
        'name': 'landing:consent',
        'priority': 0.4,
        'changefreq': 'yearly',
    },
    {
        'name': 'landing:terms',
        'priority': 0.5,
        'changefreq': 'monthly',
    },
    {
        'name': 'landing:offer',
        'priority': 0.6,
        'changefreq': 'monthly',
    },
    {
        'name': 'landing:license',
        'priority': 0.6,
        'changefreq': 'monthly',
    },
)


class LandingSitemap(Sitemap):
    """All indexable public URLs of the site."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parsed = urlparse(settings.SITE_URL)
        self.protocol = parsed.scheme or 'https'

    def items(self):
        return PUBLIC_PAGES

    def location(self, item):
        return reverse(item['name'])

    def priority(self, item):
        return item['priority']

    def changefreq(self, item):
        return item['changefreq']

    def lastmod(self, item):
        return timezone.now().date()
