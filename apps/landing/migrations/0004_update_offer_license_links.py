"""Update footer links for public offer and license pages."""
from django.db import migrations


def update_links(apps, schema_editor):
    SiteLink = apps.get_model('landing', 'SiteLink')
    updates = {
        'Публичная оферта': '/legal/offer/',
        'Политика конфиденциальности': '/legal/privacy/',
        'Акции, бонусы и оплата': '/legal/license/',
    }
    for label, href in updates.items():
        SiteLink.objects.filter(group='footer_doc', label=label).update(href=href)


def revert_links(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_update_legal_links'),
    ]

    operations = [
        migrations.RunPython(update_links, revert_links),
    ]
