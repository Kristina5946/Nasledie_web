from django.urls import path

from apps.analytics.views import track_client_event

app_name = 'analytics'

urlpatterns = [
    path('track/', track_client_event, name='track'),
]
