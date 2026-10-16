from django_ckeditor_5.fields import CKEditor5Field
from django.db import models


class NewsCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='Названия категории')

    class Meta:
        verbose_name = 'Категория новости'
        verbose_name_plural = 'Категории новостей'

    def __str__(self):
        return self.title



class News(models.Model):
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name='Категория новости'
    )
    title = models.CharField(max_length=255, verbose_name='Названия новости')
    text = CKEditor5Field(config_name='default', verbose_name='Описание')
    image = models.ImageField(
        upload_to='news/',
        blank=True,
        null=True,
        verbose_name='Изображения',
    )
    is_popular = models.BooleanField(
        default=False,
        verbose_name='Популярен ли?',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title


class NewsGallery(models.Model):

    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='gallery',
        verbose_name='Новость'
    )
    image = models.ImageField(
        upload_to='news_gallery/',
        verbose_name='Галерея Изображения',
    )

    class Meta:
        verbose_name = 'Галерея новости'
        verbose_name_plural = 'Галерея новостей'
