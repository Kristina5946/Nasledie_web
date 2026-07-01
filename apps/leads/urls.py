from django.urls import path

from apps.leads.views import submit_contact_lead

app_name = 'leads'

urlpatterns = [
    path('leads/contact/', submit_contact_lead, name='contact_submit'),
]
