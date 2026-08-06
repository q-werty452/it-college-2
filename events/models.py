from django.db import models


class OpenDay(models.Model):
    title = models.CharField(max_length=255, verbose_name='Названия')
    date = models.DateField(verbose_name='Дата')
    time = models.CharField(max_length=100, verbose_name='Время')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'День открытых дверей'
        verbose_name_plural = 'День открытых дверей'
        ordering = ['date']



class OpenDayFeature(models.Model):
    title = models.CharField(max_length=255, verbose_name='Названия')
    description = models.TextField(verbose_name='Описание')
    icon_class = models.CharField(
        max_length=100,
        verbose_name='CSS класс иконки',
        help_text='Например: fab fa-telegram или bi bi-telegram',
        default='fab fa-telegram',
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Что вас ждет'
        verbose_name_plural = 'Что вас ждет'
        ordering = ['order']