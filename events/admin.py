from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from events.models import OpenDay, OpenDayFeature


@admin.register(OpenDay)
class OpenDayAdmin(TranslationAdmin):
    list_display = ('title', 'date', 'time')


@admin.register(OpenDayFeature)
class OpenDayFeatureAdmin(TranslationAdmin):
    list_display = ('title', 'description', 'order')

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
                'css/icon-picker.css',
            )
        }
        js = ('js/icon-picker.js',)

