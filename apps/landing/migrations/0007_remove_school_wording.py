"""Remove school/family-class wording and refresh FAQ copy."""
from django.db import migrations


FAQ_UPDATES = {
    'Чем ваш подход отличается от обычной школы?': (
        'Чем ваш подход отличается от массового образования?',
        'В привычном формате все подстраиваются под единый темп программы. '
        'Мы строим маршрут обучения вокруг талантов самого ребёнка: кто-то мыслит формулами, '
        'кто-то — красками и звуками, кому-то важно двигаться и конструировать. '
        'Наша задача — не переделать ребёнка под стандарт, а разглядеть искру внутри '
        'и дать ей инструменты для роста.',
    ),
    'Ставят ли в вашей школе двойки и задают ли домашнее задание?': (
        'Ставят ли двойки и много ли домашнего задания?',
        'Мы учим без стресса, поэтому у нас нет «двоек» и ежедневных контрольных работ. Оценки '
        'используются исключительно для мотивации и подведения итогов. Домашние задания задаются для '
        'закрепления материала, они творческие, интересные и рассчитаны на то, чтобы ребёнок справлялся '
        'без помощи родителей. Для отслеживания заданий предусмотрено собственное приложение.',
    ),
    'Безопасно ли ребенку находиться в центре?': (
        'Безопасно ли ребёнку находиться в центре?',
        'Мы обеспечиваем полную безопасность: в помещениях установлено видеонаблюдение, охранная '
        'сигнализация и тревожная кнопка. Кроме того, мы заботимся о ментальном здоровье учеников — '
        'в штате работает психолог, а атмосфера в группах исключает травлю и буллинг.',
    ),
}

NEW_FAQ = (
    'Как устроено обучение в центре?',
    'Мы работаем в небольших группах (до 10 человек) по индивидуальным программам. '
    'Родители могут выбрать очный формат занятий в центре — с вниманием к каждому ребёнку '
    'и комфортным темпом без давления массового образования.',
)

DIRECTOR_MESSAGE = (
    'Приходите знакомиться: покажем уютные учебные пространства с современной мебелью — '
    'вы почувствуете атмосферу искреннего участия и профессионального тепла.'
)


def clean_school_wording(apps, schema_editor):
    Director = apps.get_model('landing', 'Director')
    FaqItem = apps.get_model('landing', 'FaqItem')

    director = Director.objects.filter(pk=1).first()
    if director:
        director.message = DIRECTOR_MESSAGE
        director.save()

    FaqItem.objects.filter(question='Что такое семейные классы?').delete()

    for old_question, (new_question, new_answer) in FAQ_UPDATES.items():
        FaqItem.objects.filter(question=old_question).update(
            question=new_question,
            answer=new_answer,
        )

    if not FaqItem.objects.filter(question=NEW_FAQ[0]).exists():
        max_order = FaqItem.objects.order_by('-sort_order').values_list('sort_order', flat=True).first() or 0
        FaqItem.objects.create(
            question=NEW_FAQ[0],
            answer=NEW_FAQ[1],
            sort_order=max_order + 1,
            is_published=True,
        )

    # Re-pack sort order after deletions
    for order, item in enumerate(FaqItem.objects.filter(is_published=True).order_by('sort_order', 'pk')):
        if item.sort_order != order:
            item.sort_order = order
            item.save(update_fields=['sort_order'])


def revert_clean(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0006_move_director_text_to_faq'),
    ]

    operations = [
        migrations.RunPython(clean_school_wording, revert_clean),
    ]
