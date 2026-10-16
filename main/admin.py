from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin

from main.models import DeadlineDocument, Advantage, NPACategory, NPADocument, \
    CollegeCertificate, Banner, PageHero


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag')

    def image_tag(self, obj):
        if obj.banner_image:
            return format_html(
                '<img src="{}" width="100" height="100" />',
                obj.banner_image.url
            )
        return "Нет изображения"

    image_tag.short_description = 'Превью-изображение'


@admin.register(DeadlineDocument)
class AdmissionStageAdmin(TranslationAdmin):
    list_display  = ('order', 'title', 'date_range', 'is_active')
    list_editable = ('title', 'date_range', 'is_active',)


@admin.register(Advantage)
class AdvantageAdmin(TranslationAdmin):
    list_display = ('title', 'order', 'is_active',)


@admin.register(NPACategory)
class NPACategoryAdmin(TranslationAdmin):
    list_display = ('title', 'order',)


@admin.register(NPADocument)
class NPADocumentAdmin(TranslationAdmin):
    list_display = ('title', 'order',)


@admin.register(CollegeCertificate)
class CollegeCertificateAdmin(TranslationAdmin):
    list_display = ('ribbon_text', 'org_name',)


@admin.register(PageHero)
class PageHeroAdmin(TranslationAdmin):
    list_display = ('page', 'title')
