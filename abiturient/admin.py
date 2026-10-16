from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from abiturient.models import FAQ, RequiredDocument, SubmitDocument, InfoCard
from core.admin_mixins import ReadOnlySubmissionAdminMixin


@admin.register(RequiredDocument)
class RequiredDocumentAdmin(TranslationAdmin):
    list_display = ('title', 'order')



@admin.register(SubmitDocument)
class SubmitDocumentAdmin(ReadOnlySubmissionAdminMixin, admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'program', 'study_form', 'phone', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'program', 'study_form', 'form_of_study', 'citizenship', 'created_at')
    search_fields = ('first_name', 'last_name', 'middle_name', 'phone', 'email')
    date_hierarchy = 'created_at'



@admin.register(InfoCard)
class InfoCardAdmin(TranslationAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
                'css/icon-picker.css',
            )
        }
        js = ('js/icon-picker.js',)



@admin.register(FAQ)
class FAQItemAdmin(TranslationAdmin):
    list_display = ('question', 'order', 'is_popular')
