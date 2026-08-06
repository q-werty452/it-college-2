from modeltranslation.translator import register, TranslationOptions

from events.models import OpenDay, OpenDayFeature


@register(OpenDay)
class OpenDayTranslationOptions(TranslationOptions):
    fields = ('title','date',)


@register(OpenDayFeature)
class OpenDayFeatureTranslationOptions(TranslationOptions):
    fields = ('title','description',)