"""Static landing page content (can be moved to DB later)."""

BENEFITS = [
    {
        'icon': '👨‍🏫',
        'title': 'Индивидуальный подход',
        'description': (
            'Малые классы позволяют уделить внимание каждому ученику. '
            'Никто не остается незамеченным, материал усваивается на 100%.'
        ),
        'color': 'purple',
    },
    {
        'icon': '📱',
        'title': 'Собственный IT-дневник',
        'description': (
            'Удобный электронный дневник, в котором родителям и детям '
            'всегда четко видно расписание, оценки и домашние задания.'
        ),
        'color': 'blue',
    },
    {
        'icon': '🧘‍♀️',
        'title': 'Учёба без стресса',
        'description': (
            'У нас нет каждодневных изнуряющих контрольных и тестов. '
            'Мы учим детей думать, а не бояться ошибиться у доски.'
        ),
        'color': 'fuchsia',
    },
]

STEPS = [
    {
        'number': 1,
        'title': 'Заявка и экскурсия',
        'description': (
            'Оставьте заявку, и мы пригласим вас на личную встречу и покажем классы.'
        ),
        'color': 'purple',
    },
    {
        'number': 2,
        'title': 'Знакомство',
        'description': (
            'Небольшое собеседование без стресса для определения уровня комфорта ребенка.'
        ),
        'color': 'fuchsia',
    },
    {
        'number': 3,
        'title': 'Зачисление',
        'description': (
            'Оформление документов и торжественное зачисление в ряды учеников.'
        ),
        'color': 'blue',
    },
]

TEACHERS = [
    {
        'name': 'Анна Иванова',
        'role': 'Преподаватель математики',
        'description': 'Учит логически мыслить и не бояться сложных задач.',
        'color': 'purple',
        'photo': 'https://placehold.co/300x300/f3e8ff/6b21a8?text=Фото',
    },
    {
        'name': 'Игорь Смирнов',
        'role': 'Преподаватель истории',
        'description': 'Превращает уроки в увлекательные путешествия во времени.',
        'color': 'blue',
        'photo': 'https://placehold.co/300x300/dbeafe/1e40af?text=Фото',
    },
    {
        'name': 'Елена Попова',
        'role': 'Учитель нач. классов',
        'description': 'Помогает сделать первые шаги в учебе уверенными.',
        'color': 'fuchsia',
        'photo': 'https://placehold.co/300x300/fae8ff/86198f?text=Фото',
    },
    {
        'name': 'Михаил Котов',
        'role': 'Физкультура и спорт',
        'description': 'Прививает любовь к активному и здоровому образу жизни.',
        'color': 'green',
        'photo': 'https://placehold.co/300x300/ecfdf5/047857?text=Фото',
    },
]

GALLERY_ITEMS = [
    {
        'title': 'Увлекательные уроки',
        'alt': 'Урок',
        'image': 'https://placehold.co/800x600/e9d5ff/6b21a8?text=Урок+в+классе',
        'col_span': 2,
        'row_span': 2,
        'title_size': '2xl',
    },
    {
        'title': 'Спортивные достижения',
        'alt': 'Спорт',
        'image': 'https://placehold.co/800x400/dbeafe/1e40af?text=Спортивные+секции',
        'col_span': 2,
        'row_span': 1,
        'title_size': 'xl',
    },
    {
        'title': 'Творчество',
        'alt': 'Творчество',
        'image': 'https://placehold.co/400x400/fae8ff/86198f?text=Творчество',
        'col_span': 1,
        'row_span': 1,
        'title_size': 'lg',
    },
    {
        'title': 'Школьный двор',
        'alt': 'Прогулки',
        'image': 'https://placehold.co/400x400/f3f4f6/374151?text=Прогулки',
        'col_span': 1,
        'row_span': 1,
        'title_size': 'lg',
    },
]

NAV_LINKS = [
    {'href': '#about', 'label': 'О нас'},
    {'href': '#benefits', 'label': 'Преимущества'},
    {'href': '#teachers', 'label': 'Педагоги'},
    {'href': '#gallery', 'label': 'Галерея'},
    {'href': '#contacts', 'label': 'Контакты'},
]

FOOTER_SCHOOL_LINKS = [
    {'href': '#about', 'label': 'О нас'},
    {'href': '#teachers', 'label': 'Наши педагоги'},
    {'href': '#benefits', 'label': 'Почему родители выбирают нас'},
    {'href': '#', 'label': 'Услуги образовательного центра'},
    {'href': '#', 'label': 'Вопрос-ответ'},
]

FOOTER_DOC_LINKS = [
    {'href': '#', 'label': 'Публичная оферта'},
    {'href': '#', 'label': 'Политика конфиденциальности'},
    {'href': '#', 'label': 'Акции, бонусы и оплата'},
]
