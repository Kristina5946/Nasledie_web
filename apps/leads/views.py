"""Lead submission API views."""
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from apps.leads.services import create_lead_from_request


@csrf_protect
@require_POST
def submit_contact_lead(request):
    lead, form = create_lead_from_request(request)
    if lead is None:
        errors = {field: errs[0] for field, errs in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    return JsonResponse({
        'success': True,
        'message': 'Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.',
        'lead_id': lead.pk,
    })
