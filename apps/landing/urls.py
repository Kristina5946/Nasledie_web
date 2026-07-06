from django.urls import path

from apps.landing.views import (
    IndexView,
    LicenseInfoView,
    PersonalDataConsentView,
    PrivacyPolicyView,
    PublicOfferView,
    TermsOfUseView,
)

app_name = 'landing'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('legal/privacy/', PrivacyPolicyView.as_view(), name='privacy'),
    path('legal/consent/', PersonalDataConsentView.as_view(), name='consent'),
    path('legal/terms/', TermsOfUseView.as_view(), name='terms'),
    path('legal/offer/', PublicOfferView.as_view(), name='offer'),
    path('legal/license/', LicenseInfoView.as_view(), name='license'),
]
