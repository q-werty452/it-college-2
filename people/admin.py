from django.contrib import admin

from people.models import Director, Graduates, GraduateGallery, Partner, \
    SiteStats
from modeltranslation.admin import TranslationAdmin

from core.admin_mixins import SingletonAdminMixin

class GraduateGalleryInlineAdmin(admin.TabularInline):
    model = GraduateGallery
    extra = 1


@admin.register(SiteStats)
class SiteStatsAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('employment_percent','countries_count', 'partners_count')


@admin.register(Graduates)
class GraduateAdmin(TranslationAdmin):
    list_display = ('name', 'release', 'program',)
    inlines = [GraduateGalleryInlineAdmin]


@admin.register(Partner)
class PartnerAdmin(TranslationAdmin):
    list_display = ('name','description',)

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
                'css/icon-picker.css',
            )
        }
        js = ('js/icon-picker.js',)


@admin.register(Director)
class DirectorAdmin(SingletonAdminMixin, TranslationAdmin):
    list_display = ('name','description')
