"""Landing page views."""
from django.views.generic import TemplateView

from apps.landing.services import get_landing_context


class IndexView(TemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_landing_context())
        return context
