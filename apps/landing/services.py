"""Landing page data providers."""
import json

from django.db.models import Prefetch

from apps.landing.data import BENEFITS, STEPS, TUTORING_SERVICES
from apps.landing.models import (
    Director,
    FaqItem,
    GalleryItem,
    PricingPlan,
    PricingTier,
    SiteLink,
    Teacher,
)


def _published(queryset):
    return queryset.filter(is_published=True)


def build_pricing_tiers():
    tiers = {}
    for tier in (
        PricingTier.objects.filter(is_published=True)
        .prefetch_related(
            Prefetch(
                'plans',
                queryset=PricingPlan.objects.filter(is_published=True).order_by('sort_order', 'pk'),
            )
        )
        .order_by('sort_order', 'pk')
    ):
        tiers[tier.slug] = {
            'label': tier.label,
            'note': tier.note,
            'plans': [
                {
                    'title': plan.title,
                    'price': plan.price,
                    'original': plan.original_price or None,
                    'icon': plan.icon,
                }
                for plan in tier.plans.all()
            ],
        }
    return tiers


def get_landing_context():
    director = Director.objects.prefetch_related('highlights').first()
    pricing_tiers = build_pricing_tiers()

    return {
        'benefits': BENEFITS,
        'steps': STEPS,
        'director': director,
        'teachers': list(_published(Teacher.objects.all())),
        'tutoring_services': TUTORING_SERVICES,
        'pricing_tiers': pricing_tiers,
        'pricing_tiers_json': json.dumps(pricing_tiers, ensure_ascii=False),
        'gallery_items': list(_published(GalleryItem.objects.all())),
        'faq_items': list(_published(FaqItem.objects.all())),
        'enrollment_year': '2026/2027',
    }


def get_site_links(group):
    return list(
        _published(SiteLink.objects.filter(group=group)).values('href', 'label')
    )
