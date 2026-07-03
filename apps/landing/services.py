"""Landing page data providers."""
import json

from apps.landing.data import (
    BENEFITS,
    DIRECTOR,
    FAQ_ITEMS,
    FOOTER_DOC_LINKS,
    FOOTER_SCHOOL_LINKS,
    GALLERY_ITEMS,
    NAV_LINKS,
    PRICING_TIERS,
    STEPS,
    TEACHERS,
    TUTORING_SERVICES,
)


def get_landing_context():
    return {
        'benefits': BENEFITS,
        'steps': STEPS,
        'director': DIRECTOR,
        'teachers': TEACHERS,
        'tutoring_services': TUTORING_SERVICES,
        'pricing_tiers': PRICING_TIERS,
        'pricing_tiers_json': json.dumps(PRICING_TIERS, ensure_ascii=False),
        'gallery_items': GALLERY_ITEMS,
        'faq_items': FAQ_ITEMS,
        'nav_links': NAV_LINKS,
        'footer_school_links': FOOTER_SCHOOL_LINKS,
        'footer_doc_links': FOOTER_DOC_LINKS,
        'enrollment_year': '2026/2027',
    }
