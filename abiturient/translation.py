
from modeltranslation.translator import register, TranslationOptions

from abiturient.models import RequiredDocument, FAQ, InfoCard


@register(RequiredDocument)
class RequiredDocumentTranslationOptions(TranslationOptions):
    fields = ('title','description')


@register(InfoCard)
class InfoCardTranslationOptions(TranslationOptions):
    fields = ('title','description')

@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question','content')
