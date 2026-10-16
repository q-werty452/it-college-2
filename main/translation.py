from modeltranslation.translator import register, TranslationOptions

from main.models import DeadlineDocument, Advantage, NPACategory, NPADocument, \
    CollegeCertificate, PageHero


@register(DeadlineDocument)
class DeadlineDocument(TranslationOptions):
    fields = ('title', 'date_range')



@register(Advantage)
class Advantage(TranslationOptions):
    fields = ('title', 'description',)


@register(NPACategory)
class NPACategory(TranslationOptions):
    fields = ('title',)


@register(NPADocument)
class NPADocument(TranslationOptions):
    fields = ('title',)


@register(CollegeCertificate)
class CollegeCertificate(TranslationOptions):
    fields = ('org_name', 'title', 'subtitle', 'badge_text')

@register(PageHero)
class PageHero(TranslationOptions):
    fields = ('title', 'subtitle')
