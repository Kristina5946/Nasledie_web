"""Editable landing page content stored in the database."""
from django.db import models
from image_cropping import ImageRatioField


COLOR_CHOICES = [
    ('purple', 'Фиолетовый'),
    ('blue', 'Синий'),
    ('fuchsia', 'Фуксия'),
    ('indigo', 'Индиго'),
    ('green', 'Зелёный'),
]

GALLERY_TITLE_SIZE_CHOICES = [
    ('lg', 'Малый'),
    ('xl', 'Средний'),
    ('2xl', 'Крупный'),
]

GALLERY_GRID_CHOICES = [
    ('md:col-span-1', '1 колонка'),
    ('md:col-span-2', '2 колонки'),
    ('md:col-span-2 md:row-span-2', '2×2 (крупная)'),
]

SITE_LINK_GROUP_CHOICES = [
    ('nav', 'Шапка сайта'),
    ('footer_school', 'Футер — о центре'),
    ('footer_doc', 'Футер — документы'),
]


class OrderedModel(models.Model):
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0, db_index=True)
    is_published = models.BooleanField('Показывать на сайте', default=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['sort_order', 'pk']


class SiteContact(models.Model):
    """Контакты центра — используются в блоке контактов, карте и футере."""

    phone = models.CharField('Телефон', max_length=32)
    email = models.EmailField('E-mail')
    address = models.CharField('Адрес', max_length=255)
    vk_url = models.URLField('Ссылка ВКонтакте')
    vk_label = models.CharField('Подпись VK', max_length=64, default='darovanie34')
    yandex_map_script = models.TextField(
        'Код карты Яндекс',
        help_text='Вставьте script из конструктора карт Яндекса.',
    )
    map_status = models.CharField('Статус на карте', max_length=64, default='Мы открыты')
    legacy_url = models.URLField('Ссылка на старый сайт', blank=True)
    footer_tagline = models.TextField(
        'Описание в футере',
        default=(
            'Образовательный центр, где учеба в радость. '
            'Индивидуальный подход и комфортная среда для каждого ребенка.'
        ),
    )

    class Meta:
        verbose_name = 'Контакты сайта'
        verbose_name_plural = 'Контакты сайта'

    def __str__(self):
        return self.phone

    @property
    def phone_href(self):
        digits = ''.join(char for char in self.phone if char.isdigit())
        if digits.startswith('8'):
            digits = f'7{digits[1:]}'
        return f'tel:+{digits}'

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                'phone': '+7 (995) 134-50-50',
                'email': 'skeseniya@bk.ru',
                'address': 'г. Волгоград, ул. имени Ивана Морозова, 5, этаж 1',
                'vk_url': 'https://vk.com/darovanie34',
                'yandex_map_script': (
                    '<script type="text/javascript" charset="utf-8" async '
                    'src="https://api-maps.yandex.ru/services/constructor/1.0/js/'
                    '?um=constructor%3A883665ff883f454c18651416af02039f40c66e4801ea3c4adb85860b58b11224'
                    '&amp;width=100%25&amp;height=100%25&amp;lang=ru_RU&amp;scroll=true"></script>'
                ),
            },
        )
        return obj


class Director(models.Model):
    """Блок директора на главной."""

    name = models.CharField('ФИО', max_length=200)
    role = models.CharField('Должность', max_length=200)
    quote = models.TextField('Цитата')
    photo = models.ImageField('Фото', upload_to='content/director/')
    photo_cropping = ImageRatioField(
        'photo',
        '400x500',
        size_warning=True,
        verbose_name='Кадрирование фото',
        help_text='Выберите область фото для блока директора.',
    )

    class Meta:
        verbose_name = 'Директор'
        verbose_name_plural = 'Директор'

    def __str__(self):
        return self.name


class DirectorHighlight(models.Model):
    director = models.ForeignKey(
        Director,
        on_delete=models.CASCADE,
        related_name='highlights',
        verbose_name='Директор',
    )
    text = models.CharField('Пункт', max_length=255)
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Преимущество директора'
        verbose_name_plural = 'Преимущества директора'
        ordering = ['sort_order', 'pk']

    def __str__(self):
        return self.text


class FaqItem(OrderedModel):
    question = models.CharField('Вопрос', max_length=500)
    answer = models.TextField('Ответ')

    class Meta(OrderedModel.Meta):
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопрос-ответ'

    def __str__(self):
        return self.question


class Teacher(OrderedModel):
    name = models.CharField('ФИО', max_length=200)
    role = models.CharField('Должность / предмет', max_length=200)
    description = models.TextField('Описание')
    color = models.CharField('Цвет акцента', max_length=16, choices=COLOR_CHOICES, default='purple')
    photo = models.ImageField('Фото', upload_to='content/teachers/')
    avatar_cropping = ImageRatioField(
        'photo',
        '400x400',
        size_warning=True,
        verbose_name='Кадрирование аватара',
        help_text='Выберите область фото для круглого аватара в слайдере.',
    )

    class Meta(OrderedModel.Meta):
        verbose_name = 'Педагог'
        verbose_name_plural = 'Педагоги'

    def __str__(self):
        return self.name


class PricingTier(models.Model):
    slug = models.SlugField('Код', max_length=16, unique=True, help_text='Например: 1-4 или 5-9')
    label = models.CharField('Подпись фильтра', max_length=64)
    note = models.TextField('Примечание под тарифами')
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_published = models.BooleanField('Показывать', default=True)

    class Meta:
        verbose_name = 'Группа тарифов'
        verbose_name_plural = 'Группы тарифов'
        ordering = ['sort_order', 'pk']

    def __str__(self):
        return self.label


class PricingPlan(models.Model):
    tier = models.ForeignKey(
        PricingTier,
        on_delete=models.CASCADE,
        related_name='plans',
        verbose_name='Группа',
    )
    title = models.CharField('Название', max_length=120)
    price = models.CharField('Цена', max_length=32, help_text='Например: 25 000')
    original_price = models.CharField('Старая цена', max_length=32, blank=True)
    icon = models.CharField('Иконка', max_length=8, default='📅')
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_published = models.BooleanField('Показывать', default=True)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        ordering = ['sort_order', 'pk']

    def __str__(self):
        return f'{self.tier.label} — {self.title}'


class GalleryItem(OrderedModel):
    title = models.CharField('Заголовок', max_length=120)
    alt_text = models.CharField('Alt-текст', max_length=200)
    image = models.ImageField('Фото', upload_to='content/gallery/')
    image_cropping = ImageRatioField(
        'image',
        '1200x800',
        free_crop=True,
        size_warning=True,
        verbose_name='Кадрирование фото',
        help_text='Выберите фрагмент для отображения в сетке галереи.',
    )
    grid_class = models.CharField(
        'Размер в сетке',
        max_length=64,
        choices=GALLERY_GRID_CHOICES,
        default='md:col-span-1',
    )
    title_size = models.CharField(
        'Размер заголовка',
        max_length=8,
        choices=GALLERY_TITLE_SIZE_CHOICES,
        default='lg',
    )

    class Meta(OrderedModel.Meta):
        verbose_name = 'Фото галереи'
        verbose_name_plural = 'Галерея'

    def __str__(self):
        return self.title


class SiteLink(OrderedModel):
    group = models.CharField('Раздел', max_length=20, choices=SITE_LINK_GROUP_CHOICES, db_index=True)
    label = models.CharField('Текст ссылки', max_length=120)
    href = models.CharField('URL / якорь', max_length=200)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Ссылка сайта'
        verbose_name_plural = 'Ссылки сайта'

    def __str__(self):
        return f'{self.get_group_display()}: {self.label}'
