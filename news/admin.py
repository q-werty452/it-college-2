from django.contrib import admin

from news.models import NewsCategory, News, NewsGallery
from modeltranslation.admin import TranslationAdmin


class NewsGalleryInlineAdmin(admin.TabularInline):
    model = NewsGallery
    extra = 1

@admin.register(NewsCategory)
class NewsCategoryAdmin(TranslationAdmin):
    list_display = ('title',)


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('title', 'category', 'image')
    inlines = [NewsGalleryInlineAdmin]

