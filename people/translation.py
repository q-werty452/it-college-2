from modeltranslation.translator import register, TranslationOptions

from people.models import Graduates, Partner, Director


@register(Graduates)
class Graduates(TranslationOptions):
    fields = ('name','release', 'short_description','full_description', 'achievements', 'story')


@register(Partner)
class Partner(TranslationOptions):
    fields = ('name', 'description',)



@register(Director)
class Director(TranslationOptions):
    fields = ('name', 'description',)