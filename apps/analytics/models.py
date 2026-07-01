"""Analytics models for traffic and promotion metrics."""
from django.db import models


class PageView(models.Model):
    class EventType(models.TextChoices):
        PAGE_VIEW = 'page_view', 'Просмотр страницы'
        CTA_CLICK = 'cta_click', 'Клик по CTA'
        FORM_START = 'form_start', 'Начало заполнения формы'
        THEME_TOGGLE = 'theme_toggle', 'Переключение темы'

    path = models.CharField('Путь', max_length=255, db_index=True)
    event_type = models.CharField(
        'Тип события',
        max_length=20,
        choices=EventType.choices,
        default=EventType.PAGE_VIEW,
        db_index=True,
    )
    session_key = models.CharField('Сессия', max_length=64, blank=True, db_index=True)

    utm_source = models.CharField('UTM Source', max_length=100, blank=True, db_index=True)
    utm_medium = models.CharField('UTM Medium', max_length=100, blank=True)
    utm_campaign = models.CharField('UTM Campaign', max_length=150, blank=True, db_index=True)
    referrer = models.URLField('Реферер', max_length=500, blank=True)
    user_agent = models.CharField('User Agent', max_length=500, blank=True)
    ip_address = models.GenericIPAddressField('IP-адрес', null=True, blank=True)

    metadata = models.JSONField('Метаданные', default=dict, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Событие аналитики'
        verbose_name_plural = 'События аналитики'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['path', 'created_at']),
            models.Index(fields=['utm_campaign', 'created_at']),
        ]

    def __str__(self):
        return f'{self.get_event_type_display()} — {self.path}'
