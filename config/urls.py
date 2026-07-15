"""Root URL configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import RedirectView

from apps.landing.sitemaps import LandingSitemap
from apps.landing.views import robots_txt

sitemaps = {
    'pages': LandingSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'favicon.ico',
        RedirectView.as_view(url=f'{settings.STATIC_URL}images/logo.png', permanent=True),
        name='favicon',
    ),
    path('robots.txt', robots_txt, name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('', include('apps.landing.urls', namespace='landing')),
    path('api/', include('apps.leads.urls', namespace='leads')),
    path('api/analytics/', include('apps.analytics.urls', namespace='analytics')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
