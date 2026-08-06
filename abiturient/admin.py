from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from abiturient.models import FAQ, RequiredDocument, SubmitDocument, InfoCard


@admin.register(RequiredDocument)
class RequiredDocument(TranslationAdmin):
    list_display = ('title', 'order')



@admin.register(SubmitDocument)
class SubmitDocument(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email')



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
