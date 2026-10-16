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



class Staff(models.Model):
    DEPARTMENT_CHOICES = [
        ('it', 'ИТ-кафедра'),
        ('general', 'Общеобразовательные предметы'),
        ('admin', 'Администрация'),
        ('support', 'Вспомогательный персонал'),
    ]

    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    position = models.CharField(max_length=200, verbose_name='Должность')
    department = models.CharField(
        max_length=20,
        choices=DEPARTMENT_CHOICES,
        default='it',
        verbose_name='Отдел',
    )
    is_leadership = models.BooleanField(
        default=False,
        verbose_name='Руководящий состав',
        help_text='Показывать в карусели «Руководящий состав». '
                  'Первый по порядку показывается крупно вверху страницы.',
    )
    photo = models.ImageField(
        upload_to='staff/',
        blank=True,
        verbose_name='Фото',
    )
    experience = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Стаж',
        help_text='Например: 9 лет',
    )
    education = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Образование',
    )
    tags = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Метки',
        help_text='Через запятую, например: Канд. пед. наук, Методист',
    )
    short_bio = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Коротко о сотруднике',
        help_text='Текст на карточке руководства',
    )
    bio = models.TextField(blank=True, verbose_name='О сотруднике')
    courses = models.TextField(
        blank=True,
        verbose_name='Преподаваемые дисциплины',
        help_text='Каждая дисциплина с новой строки',
    )
    achievements = models.TextField(
        blank=True,
        verbose_name='Достижения',
        help_text='Каждое достижение с новой строки',
    )
    email = models.EmailField(blank=True, verbose_name='Электронная почта')
    phone = models.CharField(max_length=30, blank=True, verbose_name='Телефон')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Показывать на сайте')

    class Meta:
        ordering = ['order', 'full_name']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.full_name

    @staticmethod
    def _lines(text):
        return [line.strip() for line in text.splitlines() if line.strip()]

    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    @property
    def course_list(self):
        return self._lines(self.courses)

    @property
    def achievement_list(self):
        return self._lines(self.achievements)



class StaffGallery(models.Model):
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name='gallery',
        verbose_name='Сотрудник',
    )
    image = models.ImageField(upload_to='staff_gallery/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Фото сотрудника'
        verbose_name_plural = 'Галерея сотрудника'
