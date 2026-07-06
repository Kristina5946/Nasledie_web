"""Populate landing content from the original static data."""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.db import migrations


def _static_path(relative_path):
    return Path(settings.BASE_DIR) / 'static' / relative_path


def _attach_image(instance, field_name, static_relative):
    path = _static_path(static_relative)
    if not path.exists():
        return
    field = getattr(instance, field_name)
    with path.open('rb') as image_file:
        field.save(path.name, File(image_file), save=False)


def load_initial_content(apps, schema_editor):
    SiteContact = apps.get_model('landing', 'SiteContact')
    Director = apps.get_model('landing', 'Director')
    DirectorHighlight = apps.get_model('landing', 'DirectorHighlight')
    FaqItem = apps.get_model('landing', 'FaqItem')
    Teacher = apps.get_model('landing', 'Teacher')
    PricingTier = apps.get_model('landing', 'PricingTier')
    PricingPlan = apps.get_model('landing', 'PricingPlan')
    GalleryItem = apps.get_model('landing', 'GalleryItem')
    SiteLink = apps.get_model('landing', 'SiteLink')

    SiteContact.objects.update_or_create(
        pk=1,
        defaults={
            'phone': '+7 (995) 134-50-50',
            'email': 'skeseniya@bk.ru',
            'address': 'г. Волгоград, ул. имени Ивана Морозова, 5, этаж 1',
            'vk_url': 'https://vk.com/darovanie34',
            'vk_label': 'darovanie34',
            'legacy_url': 'https://nasledie34.insales.site/',
            'map_status': 'Мы открыты',
            'footer_tagline': (
                'Образовательный центр, где учеба в радость. '
                'Индивидуальный подход и комфортная среда для каждого ребенка.'
            ),
            'yandex_map_script': (
                '<script type="text/javascript" charset="utf-8" async '
                'src="https://api-maps.yandex.ru/services/constructor/1.0/js/'
                '?um=constructor%3A883665ff883f454c18651416af02039f40c66e4801ea3c4adb85860b58b11224'
                '&amp;width=100%25&amp;height=100%25&amp;lang=ru_RU&amp;scroll=true"></script>'
            ),
        },
    )

    director, _ = Director.objects.update_or_create(
        pk=1,
        defaults={
            'name': 'Гелунова Наталья Владимировна',
            'role': 'Директор образовательного центра',
            'quote': (
                'Мы создали пространство, где ребёнок чувствует себя услышанным. '
                '«Наследие» — это не только знания, но и уверенность, интерес к учёбе '
                'и уважение к личности каждого ученика.'
            ),
        },
    )
    _attach_image(director, 'photo', 'images/teachers/Гелунова.jpg')
    director.save()

    DirectorHighlight.objects.filter(director=director).delete()
    for order, text in enumerate([
        'Директор и учитель русского языка и литературы',
        'Индивидуальные траектории обучения',
        'Сильная команда педагогов и наставников',
    ]):
        DirectorHighlight.objects.create(director=director, text=text, sort_order=order)

    faq_data = [
        (
            'Что такое семейные классы?',
            'Это современный формат образования, при котором родители переводят ребенка на семейное '
            'обучение. Вы поручаете нашему центру проведение занятий по индивидуальной программе '
            'в комфортных малочисленных классах (не более 10 учеников).',
        ),
        (
            'По какому графику учатся дети?',
            'Наш учебный год длится с сентября по май и делится на модули: 5 недель учебы чередуются '
            'с 1 неделей каникул, что позволяет детям не переутомляться. Занятия 1-3 классов начинаются '
            'в 9:15 (3-5 уроков в день), а 5-7 классов — в 9:00 (5-6 уроков в день). Длительность одного '
            'урока составляет 35 минут.',
        ),
        (
            'Ставят ли в вашей школе двойки и задают ли домашнее задание?',
            'Мы учим без стресса, поэтому у нас нет «двоек» и ежедневных контрольных работ. Оценки '
            'используются исключительно для мотивации и подведения итогов. Домашние задания задаются для '
            'закрепления материала, они творческие, интересные и рассчитаны на то, чтобы ребенок справлялся '
            'без помощи родителей. Для отслеживания заданий предусмотрено собственное приложение.',
        ),
        (
            'Как организовано питание в центре?',
            'Питание для учеников организует наш партнер — ООО «Обедов», который работает на рынке '
            'Волгограда с 2019 года и имеет все сертификаты соответствия на продукцию. В меню представлены '
            'качественные горячие блюда (например, куриные отбивные, котлеты по-киевски), выпечка, сэндвичи '
            'и мини-шаурма. Также доступен выгодный «Специальный сет», который включает блюдо из меню и '
            'натуральный напиток на выбор.',
        ),
        (
            'Нужно ли нанимать репетиторов для подготовки к аттестации?',
            'Нет, мы сами подготавливаем детей к аттестации и ВПР прямо во время учебного процесса, '
            'без привлечения репетиторов. Сама аттестация проходит в апреле через нашу лицензированную '
            'организацию-партнёра, что дает возможность получать документы государственного образца.',
        ),
        (
            'Можно ли оплатить обучение материнским капиталом?',
            'Да. Образовательный центр «Наследие» работает на основании официальной лицензии '
            '(№ Л035-01239-34/04540213). Благодаря этому вы можете использовать материнский капитал, '
            'а также оформить налоговый вычет за обучение, что значительно сократит ваши расходы.',
        ),
        (
            'Безопасно ли ребенку находиться в центре?',
            'Мы обеспечиваем полную безопасность: в помещениях установлено видеонаблюдение, охранная '
            'сигнализация и тревожная кнопка. Кроме того, мы заботимся о ментальном здоровье учеников — '
            'в штате работает психолог, а атмосфера в классах исключает травлю и буллинг.',
        ),
        (
            'Как поступить в центр «Наследие»?',
            'Для поступления нужно сделать четыре шага: записаться на собеседование по телефону или онлайн, '
            'прийти к нам на экскурсию для знакомства руководителя с родителем, пройти диагностику ребенка '
            '(академические знания и работа с психологом), а затем подписать договор и внести оплату. '
            'Обратите внимание, что количество мест ограничено.',
        ),
    ]
    FaqItem.objects.all().delete()
    for order, (question, answer) in enumerate(faq_data):
        FaqItem.objects.create(
            question=question,
            answer=answer,
            sort_order=order,
            is_published=True,
        )

    teachers_data = [
        {
            'name': 'Гелунова Наталья Владимировна',
            'role': 'Директор · Русский язык и литература',
            'description': 'Создаёт атмосферу доверия и помогает детям полюбить слово и чтение.',
            'color': 'purple',
            'photo': 'images/teachers/Гелунова.jpg',
        },
        {
            'name': 'Филиппова Кристина Евгеньевна',
            'role': 'Учитель информатики',
            'description': 'Превращает цифровые технологии в понятный и увлекательный предмет.',
            'color': 'blue',
            'photo': 'images/teachers/Филиппова.jpg',
        },
        {
            'name': 'Мартиросян Лусине Арменовна',
            'role': 'Учитель английского языка',
            'description': 'Развивает уверенную речь и интерес к международному общению.',
            'color': 'fuchsia',
            'photo': 'images/teachers/Мартиросян.jpg',
        },
        {
            'name': 'Парнев Сергей Николаевич',
            'role': 'Учитель физики',
            'description': 'Объясняет сложные явления простым языком и через практику.',
            'color': 'indigo',
            'photo': 'images/teachers/Парнев.jpg',
        },
    ]
    Teacher.objects.all().delete()
    for order, item in enumerate(teachers_data):
        teacher = Teacher(
            name=item['name'],
            role=item['role'],
            description=item['description'],
            color=item['color'],
            sort_order=order,
            is_published=True,
        )
        _attach_image(teacher, 'photo', item['photo'])
        teacher.save()

    pricing_data = {
        '1-4': {
            'label': '1–4 классы',
            'note': (
                'В стоимость не входит оплата учебников (разовый взнос 20 000 руб. '
                'или покупка самостоятельно) и аттестации (10 000 руб.). Возможна рассрочка.'
            ),
            'plans': [
                ('Ежемесячно', '25 000', '', '📅'),
                ('За два месяца', '48 000', '50 000', '💰'),
                ('За полугодие', '132 000', '150 000', '⏳'),
                ('За учебный год (9 месяцев)', '189 000', '225 000', '🎒'),
            ],
        },
        '5-9': {
            'label': '5–9 классы',
            'note': (
                'Можно использовать материнский капитал и оформить налоговый вычет — '
                'это поможет значительно сократить расходы.'
            ),
            'plans': [
                ('Ежемесячно', '27 000', '', '📅'),
                ('За два месяца', '52 000', '54 000', '💰'),
                ('За полугодие', '144 000', '162 000', '⏳'),
                ('За учебный год (9 мес.)', '207 000', '243 000', '🎒'),
            ],
        },
    }
    PricingPlan.objects.all().delete()
    PricingTier.objects.all().delete()
    for tier_order, (slug, tier_info) in enumerate(pricing_data.items()):
        tier = PricingTier.objects.create(
            slug=slug,
            label=tier_info['label'],
            note=tier_info['note'],
            sort_order=tier_order,
            is_published=True,
        )
        for plan_order, (title, price, original, icon) in enumerate(tier_info['plans']):
            PricingPlan.objects.create(
                tier=tier,
                title=title,
                price=price,
                original_price=original,
                icon=icon,
                sort_order=plan_order,
                is_published=True,
            )

    gallery_data = [
        {
            'title': 'Увлекательные уроки',
            'alt_text': 'Занятия в центре «Наследие»',
            'image': 'images/photo_5350333562445568645_y.jpg',
            'grid_class': 'md:col-span-2 md:row-span-2',
            'title_size': '2xl',
        },
        {
            'title': 'Творчество',
            'alt_text': 'Творческие занятия',
            'image': 'images/photo_5350333562445568647_w.jpg',
            'grid_class': 'md:col-span-2',
            'title_size': 'xl',
        },
        {
            'title': 'Наши ученики',
            'alt_text': 'Ученики центра',
            'image': 'images/photo_5350333562445568648_w.jpg',
            'grid_class': 'md:col-span-1',
            'title_size': 'lg',
        },
        {
            'title': 'Пространство центра',
            'alt_text': 'Пространство центра',
            'image': 'images/photo_5350333562445568649_w.jpg',
            'grid_class': 'md:col-span-1',
            'title_size': 'lg',
        },
    ]
    GalleryItem.objects.all().delete()
    for order, item in enumerate(gallery_data):
        gallery_item = GalleryItem(
            title=item['title'],
            alt_text=item['alt_text'],
            grid_class=item['grid_class'],
            title_size=item['title_size'],
            sort_order=order,
            is_published=True,
        )
        _attach_image(gallery_item, 'image', item['image'])
        gallery_item.save()

    links_data = [
        ('nav', '#teachers', 'Педагоги', 0),
        ('nav', '#tutoring', 'Репетиторский центр', 1),
        ('nav', '#gallery', 'Галерея', 2),
        ('nav', '#faq', 'Вопрос-ответ', 3),
        ('nav', '#contacts', 'Контакты', 4),
        ('footer_school', '#about', 'Как поступить', 0),
        ('footer_school', '#teachers', 'Наши педагоги', 1),
        ('footer_school', '#tutoring', 'Репетиторский центр', 2),
        ('footer_school', '#pricing', 'Стоимость обучения', 3),
        ('footer_school', '#faq', 'Вопрос-ответ', 4),
        ('footer_school', '#gallery', 'Галерея', 5),
        ('footer_doc', '#', 'Публичная оферта', 0),
        ('footer_doc', '#', 'Политика конфиденциальности', 1),
        ('footer_doc', '#pricing', 'Акции, бонусы и оплата', 2),
    ]
    SiteLink.objects.all().delete()
    for group, href, label, order in links_data:
        SiteLink.objects.create(
            group=group,
            href=href,
            label=label,
            sort_order=order,
            is_published=True,
        )


def unload_initial_content(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_content, unload_initial_content),
    ]
