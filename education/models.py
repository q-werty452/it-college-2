from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

class ProgramCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Названия категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория специальности'
        verbose_name_plural = 'Категории специальностей'



class Program(models.Model):
    FORM_CHOICES = [
        ('full', _('Очная')),
        ('part', _('Заочная')),
        ('both', _('Очная и Заочная')),
    ]

    STATUS_CHOICES = [
        ('available', _('Есть места')),
        ('few', _('Мало мест')),
        ('soon', _('Скоро')),
        ('closed', _('Приём закрыт')),
    ]

    category = models.ForeignKey(
        ProgramCategory,
        on_delete=models.PROTECT,
        related_name='programs',
        verbose_name='Категория Специальности'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Названия специальности',
    )
    code = models.CharField(
        max_length=20,
        verbose_name='Код специальности',
        help_text='Например: 09.02.07',
        default='0',
    )

    duration_years = models.PositiveSmallIntegerField(
        default=3,
        verbose_name='Сколько длится обучения в годах',
    )
    duration_months = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Сколько длится обучения в месяцах',
    )

    description = RichTextField(
        blank=True,
        verbose_name='Описание',
    )
    icon_class = models.CharField(
        max_length=100,
        verbose_name='CSS класс иконки',
        default='fas fa-file-alt',
    )

    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активен ли?')

    has_budget = models.BooleanField(
        default=False,
        verbose_name='Есть ли льготы?',
    )
    benefits = models.TextField(
        default='',
        blank=True,
        verbose_name='Описание льгот',
    )
    paid_seats = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Количество контрактных мест',
    )

    study_form = models.CharField(
        max_length=10,
        choices=FORM_CHOICES,
        default='full',
        verbose_name='Форма обучения'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name='Статус приёма'
    )

    price_per_year = models.PositiveIntegerField(verbose_name='Цена в год')
    is_popular = models.BooleanField(
        default=False,
        verbose_name='Популярен ли?',
    )

    benefits_seats = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Количество льготных мест'
    )


    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def __str__(self):
        return self.name

    @property
    def duration_display(self):
        parts = []
        if self.duration_years:
            parts.append(f"{self.duration_years} г.")
        if self.duration_months:
            parts.append(f"{self.duration_months} мес.")
        return " ".join(parts)

    @property
    def price_display(self):
        return f"{self.price_per_year:,} сом/год".replace(',', ' ')



class License(models.Model):
    title = models.CharField(max_length=200, verbose_name='Названия ')
    description = models.TextField(verbose_name='Описание')
    document = models.FileField(
        upload_to='licenses/',
        blank=True,
        null=True,
        verbose_name='Документ',
    )
    icon_class = models.CharField(
        max_length=100,
        verbose_name='CSS класс иконки',
        default='fas fa-file-alt'
    )

    class Meta:
        verbose_name = 'Лицензия и аккредитация'
        verbose_name_plural = 'Лицензии и аккредитации'

    def __str__(self):
        return self.title



class TransferInfo(models.Model):
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Общая Информация'
        verbose_name_plural = 'Общая Информация'


class TransferDocument(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Названия необходимых документов',
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    def __str__(self):
        return f"{self.order}. {self.title}"

    class Meta:
        verbose_name = 'Необходимый документ'
        verbose_name_plural = 'Необходимые документы'
        ordering = ['order']
