from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from core.admin_mixins import SingletonAdminMixin

from education.models import TransferInfo, TransferDocument, ProgramCategory, \
    Program, License


@admin.register(ProgramCategory)
class SpecCategoryAdmin(TranslationAdmin):
    list_display = ('title',)


@admin.register(Program)
class ProgramAdmin(TranslationAdmin):
    list_display = (
        'name',
        'code',
        'category',
        'duration_display',
        'has_budget',
        'benefits',
        'paid_seats',
        'price_per_year',
        'is_popular',
        'is_active',
        'order',
        'benefits_seats',
    )

    list_editable = (
        'has_budget',
        'benefits',
        'paid_seats',
        'price_per_year',
        'is_active',
        'order',
    )

    list_filter = (
        'category',
        'is_active',
        'has_budget',
        'is_popular',
        'study_form',
    )
    search_fields = ('name', 'code')

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
                'css/icon-picker.css',
            )
        }
        js = ('js/icon-picker.js',)

    def duration_display(self, obj):
        return obj.duration_display

    duration_display.short_description = 'Срок'


@admin.register(License)
class LicenseAdmin(TranslationAdmin):
    list_display = ('title',)

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
                'css/icon-picker.css',
            )
        }
        js = ('js/icon-picker.js',)


@admin.register(TransferInfo)
class TransferInfoAdmin(SingletonAdminMixin, TranslationAdmin):
    list_display = ('description',)


@admin.register(TransferDocument)
class TransferDocumentAdmin(TranslationAdmin):
    list_display = ('title', 'order')
