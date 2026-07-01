"""Landing page data providers."""
from apps.landing.data import (
    BENEFITS,
    FOOTER_DOC_LINKS,
    FOOTER_SCHOOL_LINKS,
    GALLERY_ITEMS,
    NAV_LINKS,
    STEPS,
    TEACHERS,
)


def get_landing_context():
    return {
        'benefits': BENEFITS,
        'steps': STEPS,
        'teachers': TEACHERS,
        'gallery_items': GALLERY_ITEMS,
        'nav_links': NAV_LINKS,
        'footer_school_links': FOOTER_SCHOOL_LINKS,
        'footer_doc_links': FOOTER_DOC_LINKS,
        'enrollment_year': '2026/2027',
    }
