"""Director extended bio fields and updated content."""
from django.db import migrations, models


DIRECTOR_QUOTE = (
    'За годы работы я поняла одну простую истину: никакие методики не сработают без главного — '
    'искренней любви педагога к предмету и безграничной веры в каждого ребёнка.'
)

DIRECTOR_MESSAGE = (
    'Дети чувствуют фальшь и тянутся только к тем, кто горит своим делом и видит в них личности, '
    'а не строку в журнале. В нашем центре мы знаем каждого ученика по имени, его увлечения, '
    'замечаем маленькие победы и всегда готовы подставить плечо.\n\n'
    'Моя задача как руководителя — собрать команду педагогов, которые приходят на работу с радостью, '
    'потому что горят, а не «выгорают». Мы строим маршрут обучения вокруг талантов ребёнка — '
    'не переделываем его под стандарт, а бережно поддерживаем ту искру, которая уже есть внутри.\n\n'
    'Приходите знакомиться: покажем уютные классы с современной мебелью — '
    'вы почувствуете атмосферу искреннего участия и профессионального тепла.'
)

DIRECTOR_EDUCATION = (
    'Михайловский педагогический колледж, ВГСПУ — учитель начальных классов, '
    'учитель русского языка и литературы.\n'
    'Московский институт управления — «Менеджмент. Управление персоналом».\n'
    'Курсы: Школа региональной элиты (2009); Волгоградская академия государственной службы '
    '(«Политические процессы, институты и технологии»).'
)

DIRECTOR_AWARDS = [
    'Почётная грамота и благодарность Волгоградской областной Думы',
    '«Жемчужина Волгограда» — лучший педагог по художественному слову (2022)',
    '«Жемчужина Донской волны» — лучший педагог по художественному слову (2025)',
    '«Золотые россыпи талантов» — лучший педагог, лит.-муз. композиция (2026)',
]


def update_director_content(apps, schema_editor):
    Director = apps.get_model('landing', 'Director')
    DirectorHighlight = apps.get_model('landing', 'DirectorHighlight')

    director = Director.objects.filter(pk=1).first()
    if not director:
        return

    director.quote = DIRECTOR_QUOTE
    director.message = DIRECTOR_MESSAGE
    director.education = DIRECTOR_EDUCATION
    director.save()

    DirectorHighlight.objects.filter(director=director).delete()
    for order, text in enumerate(DIRECTOR_AWARDS):
        DirectorHighlight.objects.create(
            director=director,
            text=text,
            sort_order=order,
        )


def revert_director_content(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0004_update_offer_license_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='director',
            name='education',
            field=models.TextField(blank=True, verbose_name='Образование и курсы'),
        ),
        migrations.AddField(
            model_name='director',
            name='message',
            field=models.TextField(blank=True, verbose_name='Слово директора'),
        ),
        migrations.AlterField(
            model_name='director',
            name='quote',
            field=models.TextField(
                help_text='Короткая фраза для выделения в блоке.',
                verbose_name='Краткая цитата',
            ),
        ),
        migrations.RunPython(update_director_content, revert_director_content),
    ]
