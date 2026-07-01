"""Analytics event API."""
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from apps.analytics.models import PageView
from apps.analytics.services import track_event

VALID_EVENTS = {choice[0] for choice in PageView.EventType.choices}


@csrf_protect
@require_POST
def track_client_event(request):
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    event_type = payload.get('event_type', '')
    if event_type not in VALID_EVENTS:
        return JsonResponse({'success': False, 'error': 'Invalid event type'}, status=400)

    path = payload.get('path', request.path)
    metadata = payload.get('metadata', {})

    event = track_event(request, event_type, path=path, metadata=metadata)
    return JsonResponse({'success': True, 'event_id': event.pk})
