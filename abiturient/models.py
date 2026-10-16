from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from django.db import models

from education.models import Program


class RequiredDocument(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.CharField(max_length=300, verbose_name='Описание')
    icon_svg = models.FileField(
        blank=True,
        verbose_name='SVG иконка',
        upload_to='documents/',
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Документ для поступления'
        verbose_name_plural = 'Документы для поступления'

    def __str__(self):
        return self.title



DOCUMENT_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png']
PHOTO_EXTENSIONS = ['jpg', 'jpeg', 'png']


class SubmitDocument(models.Model):
    CITIZENSHIP_CHOICES = [
        ('kg', 'Кыргызстан'),
        ('kz', 'Казахстан'),
        ('ru', 'Россия'),
        ('tj', 'Таджикистан'),
        ('other', 'Другое'),
    ]
    FORM_OF_STUDY_CHOICES = [
        ('full_time', 'Очная'),
        ('part_time', 'Заочная'),
    ]
    STUDY_FORM_CHOICES = [
        ('budget', 'Бюджет'),
        ('paid', 'Коммерция'),
    ]
    SOURCE_CHOICES = [
        ('site', 'Сайт'),
        ('social', 'Соцсети'),
        ('friends', 'Друзья'),
        ('ads', 'Реклама'),
        ('other', 'Другое'),
    ]

    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Отчество',
    )

    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Электронная почта')

    birth_date = models.DateField(verbose_name='Дата рождения')
    address = models.TextField(blank=True, verbose_name='Адрес проживания')
    citizenship = models.CharField(
        max_length=20,
        choices=CITIZENSHIP_CHOICES,
        verbose_name='Гражданство'
    )

    program = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Специальность',
    )

    form_of_study = models.CharField(
        max_length=20,
        choices=FORM_OF_STUDY_CHOICES,
        verbose_name='Форма обучения',
    )
    study_form = models.CharField(
        max_length=20,
        choices=STUDY_FORM_CHOICES,
        verbose_name='Финансирование',
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        blank=True,
        verbose_name='Откуда узнали о нас?',
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Дополнительные пожелания',
    )

    passport = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(DOCUMENT_EXTENSIONS)],
        verbose_name='Паспорт / свидетельство о рождении',
    )
    education_document = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(DOCUMENT_EXTENSIONS)],
        verbose_name='Аттестат об образовании ',
    )
    photo = models.ImageField(
        upload_to='photos/',
        validators=[FileExtensionValidator(PHOTO_EXTENSIONS)],
        verbose_name='Фото 3×4',
    )
    medical_certificate = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(DOCUMENT_EXTENSIONS)],
        blank=True,
        verbose_name='Медицинская справка 086-У',
    )

    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('done', 'Обработана'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время отправки',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Онлайн документ'
        verbose_name_plural = 'Онлайн документы'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'



class InfoCard(models.Model):
    """Карточки 'Важно знать' на странице подачи документов"""

    icon_class = models.CharField(
        max_length=100,
        verbose_name='CSS класс иконки',
        default='fas fa-info-circle',
        help_text='Например: fas fa-clock'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        ordering = ['order']
        verbose_name = 'Карточка "Важно знать"'
        verbose_name_plural = 'Карточки "Важно знать"'

    def __str__(self):
        return self.title



class FAQ(models.Model):
    question = models.CharField(max_length=200, verbose_name='Вопрос')
    content = RichTextField(verbose_name='Ответ на вопрос')
    order = models.PositiveIntegerField(verbose_name='Порядок')
    is_popular = models.BooleanField(default=False, verbose_name='Популярен ли?')

    class Meta:
        verbose_name = "Вопрос-Ответ"
        verbose_name_plural = "Вопросы и Ответы (FAQs)"
        ordering = ['order']

    def __str__(self):
        return self.question
