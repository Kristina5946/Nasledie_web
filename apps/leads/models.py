"""Lead / contact request models for conversion tracking."""
from django.db import models


class ContactLead(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_PROGRESS = 'in_progress', 'В работе'
        COMPLETED = 'completed', 'Завершена'
        REJECTED = 'rejected', 'Отклонена'

    class Source(models.TextChoices):
        LANDING = 'landing', 'Главная страница'
        POPUP = 'popup', 'Всплывающая форма'
        CALLBACK = 'callback', 'Обратный звонок'

    name = models.CharField('Имя', max_length=150)
    phone = models.CharField('Телефон', max_length=30)
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    source = models.CharField(
        'Источник',
        max_length=20,
        choices=Source.choices,
        default=Source.LANDING,
        db_index=True,
    )

    # UTM / promotion metrics
    utm_source = models.CharField('UTM Source', max_length=100, blank=True, db_index=True)
    utm_medium = models.CharField('UTM Medium', max_length=100, blank=True)
    utm_campaign = models.CharField('UTM Campaign', max_length=150, blank=True, db_index=True)
    utm_term = models.CharField('UTM Term', max_length=150, blank=True)
    utm_content = models.CharField('UTM Content', max_length=150, blank=True)
    referrer = models.URLField('Реферер', max_length=500, blank=True)
    landing_page = models.CharField('Страница', max_length=255, blank=True)
    user_agent = models.CharField('User Agent', max_length=500, blank=True)
    ip_address = models.GenericIPAddressField('IP-адрес', null=True, blank=True)

    created_at = models.DateTimeField('Создано', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.phone} ({self.get_status_display()})'
