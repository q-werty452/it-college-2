from django.db import models



class Banner(models.Model):
    banner_image = models.ImageField(
        upload_to='banner/',
        verbose_name='Изображения баннера',
    )

    class Meta:
        verbose_name = 'Изображение Баннера'
        verbose_name_plural = 'Изображения Баннера'



class DeadlineDocument(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Название этапа',
        help_text='Например: 1-й этап'
    )
    date_range = models.CharField(
        max_length=100,
        verbose_name='Период',
        help_text='Например: 1 июня — 25 июля'
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активен ли?')

    class Meta:
        ordering = ['order']
        verbose_name = 'Этап приёма'
        verbose_name_plural = 'Этапы приёма документов'

    def __str__(self):
        return f"{self.title}: {self.date_range}"


class Advantage(models.Model):
    icon_svg = models.TextField(blank=True, verbose_name='SVG иконка')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активен ли?')

    class Meta:
        ordering = ['order']
        verbose_name = 'Преимущество'
        verbose_name_plural = 'Преимущества'


class NPACategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название раздела')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Раздел НПА'
        verbose_name_plural = 'Разделы НПА'

    def __str__(self):
        return self.title


class NPADocument(models.Model):
    category = models.ForeignKey(
        NPACategory,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Раздел НПА',
    )
    title = models.CharField(max_length=300, verbose_name='Название документа')
    file = models.FileField(upload_to='npa/', verbose_name='PDF файл')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')
    is_full = models.BooleanField(default=False, verbose_name='Полный документ')

    class Meta:
        ordering = ['order']
        verbose_name = 'Документ НПА'
        verbose_name_plural = 'Документы НПА'

    def __str__(self):
        return self.title


class CollegeCertificate(models.Model):
    ribbon_text = models.CharField(
        max_length=50,
        verbose_name='Тип (Лицензия/ISO...)',
    )
    ribbon_color = models.CharField(
        max_length=20,
        default='#f59e0b',
        verbose_name='Цвет ленты (hex)'
    )
    org_name = models.CharField(max_length=200, verbose_name='Организация')
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    subtitle = models.TextField(verbose_name='Подзаголовок')
    issued_year = models.CharField(max_length=50, verbose_name='Год выдачи')
    badge_text = models.CharField(
        max_length=50,
        default='Действует',
        verbose_name='Текст бейджа',
    )
    order = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(
        upload_to='college_certificate/',
        verbose_name='Изображения паспорта',
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True, verbose_name='Активен ли?')

    class Meta:
        ordering = ['order']
        verbose_name = 'Сертификат колледжа'
        verbose_name_plural = 'Паспорт колледжа'