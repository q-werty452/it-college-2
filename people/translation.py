from modeltranslation.translator import register, TranslationOptions

from people.models import Graduates, Partner, Director, Staff


@register(Graduates)
class Graduates(TranslationOptions):
    fields = ('name','release', 'short_description','full_description', 'achievements', 'story')


@register(Partner)
class Partner(TranslationOptions):
    fields = ('name', 'description',)



@register(Director)
class Director(TranslationOptions):
    fields = ('name', 'description',)


@register(Staff)
class StaffTranslationOptions(TranslationOptions):
    fields = ('full_name', 'position', 'experience', 'education', 'tags',
              'short_bio', 'bio', 'courses', 'achievements')
