from django.db import models


class Contacts(models.Model):
    address = models.CharField(max_length=300, verbose_name='Адрес')
    phone_admission = models.CharField(
        max_length=20,
        verbose_name='Телефон Абитуриентам',
    )
    phone_students = models.CharField(
        max_length=20,
        verbose_name='Телефон Студентам',
    )
    email = models.EmailField(verbose_name='Электронная почта')
    telegram = models.CharField(max_length=100, verbose_name='Телеграмм')
    vkontakte = models.CharField(max_length=100, verbose_name='VK контакты')
    instagram = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Инстаграм',
    )
    work_hours = models.TextField(verbose_name='Режим работы')

    class Meta:
        verbose_name = 'Наш Контакт'
        verbose_name_plural = 'Наши Контакты'

    def __str__(self):
        return 'Контакты'


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='Названия отдела')
    phone_number = models.CharField(max_length=20, verbose_name='номер телефона')
    email = models.EmailField(verbose_name='Электронная почта')
    work_hours = models.TextField(verbose_name='Режим работы')
    icon_class = models.CharField(
        max_length=100,
        verbose_name='CSS класс иконки',
        help_text='Например: fab fa-telegram или bi bi-telegram',
        default='bi bi-telegram'
    )

    class Meta:
        verbose_name = 'Контакт отдела'
        verbose_name_plural = 'Контакты отделов'

    def __str__(self):
        return self.name


class ContactForm(models.Model):
    FORM_CHOICES = [
        ('select', 'Выберите тему'),
        ('faqs','Вопрос о поступлении'),
        ('info', 'Информация о программах'),
        ('price', 'Стоимость обучения '),
        ('cooperation', 'Сотрудничество'),
        ('other', 'Другое')
    ]
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone_number = models.CharField(
        max_length=20,
        verbose_name='номер телефона',
    )
    email = models.EmailField(verbose_name='Электроннач почта')
    contact_form = models.CharField(
        max_length=20,
        choices=FORM_CHOICES,
        default='select',
        verbose_name='Тема обращения',
    )
    text = models.TextField(verbose_name='Сообщение ')

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время отправки',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заявка для обратной связи'
        verbose_name_plural = 'Заявки для обратной связи'


class SocialLink(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название (Telegram, Instagram)',
    )
    url = models.URLField(verbose_name='Ссылка')
    icon_class = models.CharField(
        max_length=100,
        verbose_name='CSS класс иконки',
        help_text='Например: fab fa-telegram или bi bi-telegram'
    )
    is_active = models.BooleanField(default=True, verbose_name='')

    class Meta:
        verbose_name = 'Соцсеть'
        verbose_name_plural = 'Соцсети'

    def __str__(self):
        return self.name
