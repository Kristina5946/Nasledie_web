"""Landing page views."""
from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView

from apps.landing.services import get_landing_context


@require_GET
def robots_txt(request):
    """robots.txt for Yandex Webmaster and other search engines."""
    site_url = settings.SITE_URL.rstrip('/')
    host = urlparse(settings.SITE_URL).netloc or request.get_host()

    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /api/',
        '',
        'User-agent: Yandex',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /api/',
        f'Host: {host}',
        '',
        'User-agent: Googlebot',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /api/',
        '',
        f'Sitemap: {site_url}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines) + '\n', content_type='text/plain; charset=utf-8')


class IndexView(TemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_landing_context())
        return context


class LegalDocumentView(TemplateView):
    """Static legal document page."""

    page_title = ''
    document_heading = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['document_heading'] = self.document_heading
        return context


class PrivacyPolicyView(LegalDocumentView):
    template_name = 'legal/privacy.html'
    page_title = 'Политика конфиденциальности'
    document_heading = 'Политика конфиденциальности и обработки персональных данных'


class PersonalDataConsentView(LegalDocumentView):
    template_name = 'legal/consent.html'
    page_title = 'Согласие на обработку персональных данных'
    document_heading = 'Согласие на обработку персональных данных'


class TermsOfUseView(LegalDocumentView):
    template_name = 'legal/terms.html'
    page_title = 'Пользовательское соглашение'
    document_heading = 'Пользовательское соглашение'


class PublicOfferView(LegalDocumentView):
    template_name = 'legal/offer.html'
    page_title = 'Публичная оферта'
    document_heading = 'Публичная оферта'


class LicenseInfoView(LegalDocumentView):
    template_name = 'legal/license.html'
    page_title = 'Сведения о лицензии'
    document_heading = 'Сведения о лицензии на образовательную деятельность'
