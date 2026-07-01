"""Analytics tracking services."""
from apps.analytics.models import PageView


def get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def extract_utm_from_request(request):
    session = request.session
    utm_keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']
    utm = {}

    for key in utm_keys:
        value = request.GET.get(key, '')
        if value:
            session[key] = value
        utm[key] = session.get(key, '')

    return utm


def track_page_view(request, path=None):
    if path is None:
        path = request.path

    if path.startswith('/admin') or path.startswith('/static'):
        return None

    utm = extract_utm_from_request(request)
    return PageView.objects.create(
        path=path[:255],
        event_type=PageView.EventType.PAGE_VIEW,
        session_key=request.session.session_key or '',
        utm_source=utm.get('utm_source', ''),
        utm_medium=utm.get('utm_medium', ''),
        utm_campaign=utm.get('utm_campaign', ''),
        referrer=request.META.get('HTTP_REFERER', '')[:500],
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
        ip_address=get_client_ip(request),
    )


def track_event(request, event_type, path=None, metadata=None):
    if path is None:
        path = request.path

    utm = extract_utm_from_request(request)
    return PageView.objects.create(
        path=path[:255],
        event_type=event_type,
        session_key=request.session.session_key or '',
        utm_source=utm.get('utm_source', ''),
        utm_medium=utm.get('utm_medium', ''),
        utm_campaign=utm.get('utm_campaign', ''),
        referrer=request.META.get('HTTP_REFERER', '')[:500],
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
        ip_address=get_client_ip(request),
        metadata=metadata or {},
    )
