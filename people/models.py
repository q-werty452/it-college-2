from ckeditor.fields import RichTextField
from django.db import models

from education.models import Program



class SiteStats(models.Model):
    employment_percent = models.PositiveIntegerField(
        default=0,
        verbose_name='Трудоустройство (%)',
    )
    countries_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Стран мира'
    )
    partners_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Компаний-партнёров',
    )
    laboratories_count = models.PositiveIntegerField(
        default=0,
        verbose_name='лабораторий'
    )
    teachers = models.PositiveIntegerField(
        default=0,
        verbose_name='Преподавателей'
    )
    years_of_experience = models.PositiveIntegerField(
        default=0,
        verbose_name='Лет опыта'
    )
    students = models.PositiveIntegerField(
        default=0,
        verbose_name='Студентов'
    )

    class Meta:
        verbose_name = 'Статистика сайта'
        verbose_name_plural = 'Статистика сайта'

    def __str__(self):
        return 'Статистика'



class Graduates(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя выпускника')
    release = models.CharField(max_length=50, verbose_name='Год выпуска')
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        verbose_name='Специальность',
    )
    short_description = models.TextField(
        verbose_name='Короткая описания',
    )
    full_description = RichTextField(verbose_name='Полное описание')
    achievements = models.CharField(max_length=100, verbose_name='Достижения', default='')
    story = models.TextField(verbose_name='История', default='')
    image = models.ImageField(
        upload_to='graduates/images',
        null=True,
        blank=True,
        verbose_name='Фото выпускника',
    )

    class Meta:
        verbose_name = 'Выпускник'
        verbose_name_plural = 'Выпускники'

    def __str__(self):
        return self.name



class Partner(models.Model):
    name = models.CharField(max_length=200, verbose_name='Названия партнера')
    description = models.TextField(verbose_name='Описание')
    icon_class = models.CharField(
        max_length=100,
        verbose_name='CSS класс иконки',
        help_text='Например: fab fa-telegram или bi bi-telegram',
        default= 'fab fa-telegram',
    )

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'

    def __str__(self):
        return self.name



class GraduateGallery(models.Model):
    graduates = models.ForeignKey(
        Graduates,
        on_delete=models.CASCADE,
        verbose_name='Выпускник',
    )
    image = models.ImageField(
        upload_to='graduates_gallery/',
        verbose_name='Галерея Изображения выпускника',
    )

    class Meta:
        verbose_name = 'Галерея выпускника'
        verbose_name_plural = 'Галерея выпускников'



class Director(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя директора')
    description = RichTextField(verbose_name='Описание')
    photo = models.ImageField(
        upload_to='directors/',
        verbose_name='Изображения директора',
    )

    class Meta:
        verbose_name = 'Директор'
        verbose_name_plural = 'Директор'

    def __str__(self):
        return self.name
