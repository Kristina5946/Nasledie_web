"""Move director message paragraphs to FAQ section."""
from django.db import migrations
from django.db.models import F


DIRECTOR_MESSAGE = (
    'Приходите знакомиться: покажем уютные классы с современной мебелью — '
    'вы почувствуете атмосферу искреннего участия и профессионального тепла.'
)

NEW_FAQ_ITEMS = [
    (
        'Правда ли, что дети чувствуют фальшь?',
        'Да — и очень тонко. Они тянутся к тем, кто горит своим делом и видит в них личности, '
        'а не строку в журнале. В «Наследие» мы строим отношения на искренности: '
        'знаем каждого ученика по имени, помним его увлечения, замечаем маленькие победы '
        'и всегда готовы подставить плечо, если что-то пошло не так.',
    ),
    (
        'Как вы подбираете педагогов?',
        'Моя задача как руководителя — собрать команду, которая приходит на работу с радостью. '
        'Нам важны педагоги, которые горят, а не «выгорают», обожают учить и вдохновлять. '
        'За каждой ошибкой ребёнка мы видим не лень, а усталость или страх попробовать новое — '
        'и работаем с этим бережно.',
    ),
    (
        'Чем ваш подход отличается от обычной школы?',
        'В классической школе все подстраиваются под единый темп программы. '
        'Мы строим маршрут обучения вокруг талантов самого ребёнка: кто-то мыслит формулами, '
        'кто-то — красками и звуками, кому-то важно двигаться и конструировать. '
        'Наша задача — не переделать ребёнка под стандарт, а разглядеть искру внутри '
        'и дать ей инструменты для роста.',
    ),
]


def move_text_to_faq(apps, schema_editor):
    Director = apps.get_model('landing', 'Director')
    FaqItem = apps.get_model('landing', 'FaqItem')

    director = Director.objects.filter(pk=1).first()
    if director:
        director.message = DIRECTOR_MESSAGE
        director.save()

    FaqItem.objects.filter(is_published=True).update(
        sort_order=F('sort_order') + len(NEW_FAQ_ITEMS),
    )

    for order, (question, answer) in enumerate(NEW_FAQ_ITEMS):
        FaqItem.objects.create(
            question=question,
            answer=answer,
            sort_order=order,
            is_published=True,
        )


def revert_move(apps, schema_editor):
    FaqItem = apps.get_model('landing', 'FaqItem')

    for question, _ in NEW_FAQ_ITEMS:
        FaqItem.objects.filter(question=question).delete()

    FaqItem.objects.filter(is_published=True).update(
        sort_order=F('sort_order') - len(NEW_FAQ_ITEMS),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0005_director_bio_fields'),
    ]

    operations = [
        migrations.RunPython(move_text_to_faq, revert_move),
    ]
