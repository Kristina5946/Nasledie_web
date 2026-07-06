"""Update footer legal document links."""
from django.db import migrations


def update_legal_links(apps, schema_editor):
    SiteLink = apps.get_model('landing', 'SiteLink')
    updates = {
        'Публичная оферта': '/legal/terms/',
        'Политика конфиденциальности': '/legal/privacy/',
        'Акции, бонусы и оплата': '/legal/consent/',
    }
    for label, href in updates.items():
        SiteLink.objects.filter(group='footer_doc', label=label).update(href=href)


def revert_legal_links(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_load_initial_content'),
    ]

    operations = [
        migrations.RunPython(update_legal_links, revert_legal_links),
    ]
