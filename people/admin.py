from django.contrib import admin

from people.models import Director, Graduates, GraduateGallery, Partner, \
    SiteStats, Staff, StaffGallery
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



class StaffGalleryInlineAdmin(admin.TabularInline):
    model = StaffGallery
    extra = 1


@admin.register(Staff)
class StaffAdmin(TranslationAdmin):
    list_display = ('full_name', 'position', 'department', 'is_leadership', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('department', 'is_leadership', 'is_active')
    search_fields = ('full_name', 'position', 'email')
    inlines = [StaffGalleryInlineAdmin]
