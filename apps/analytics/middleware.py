"""Middleware for automatic page view tracking."""
from apps.analytics.services import track_page_view


class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.save()

        response = self.get_response(request)

        if request.method == 'GET' and response.status_code == 200:
            try:
                track_page_view(request)
            except Exception:
                pass

        return response
