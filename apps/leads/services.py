"""Lead submission services with UTM capture."""
from apps.leads.forms import ContactLeadForm
from apps.leads.models import ContactLead


def extract_utm_params(request):
    return {
        'utm_source': request.GET.get('utm_source', '') or request.POST.get('utm_source', ''),
        'utm_medium': request.GET.get('utm_medium', '') or request.POST.get('utm_medium', ''),
        'utm_campaign': request.GET.get('utm_campaign', '') or request.POST.get('utm_campaign', ''),
        'utm_term': request.GET.get('utm_term', '') or request.POST.get('utm_term', ''),
        'utm_content': request.GET.get('utm_content', '') or request.POST.get('utm_content', ''),
    }


def get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def create_lead_from_request(request, form_data=None):
    form = ContactLeadForm(request.POST if form_data is None else form_data)
    if not form.is_valid():
        return None, form

    lead = form.save(commit=False)
    utm = extract_utm_params(request)
    lead.utm_source = utm['utm_source']
    lead.utm_medium = utm['utm_medium']
    lead.utm_campaign = utm['utm_campaign']
    lead.utm_term = utm['utm_term']
    lead.utm_content = utm['utm_content']
    lead.referrer = request.META.get('HTTP_REFERER', '')[:500]
    lead.landing_page = request.path
    lead.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
    lead.ip_address = get_client_ip(request)
    lead.source = ContactLead.Source.LANDING
    lead.save()
    return lead, form
