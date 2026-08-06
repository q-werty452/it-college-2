
from modeltranslation.translator import register, TranslationOptions

from education.models import ProgramCategory, Program, License, TransferInfo, \
    TransferDocument


@register(ProgramCategory)
class ProgramCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Program)
class ProgramCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


@register(License)
class LicenseTranslationOptions(TranslationOptions):
    fields = ('title','document', 'description',)


@register(TransferInfo)
class TransferInfoTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(TransferDocument)
class TransferDocumentTranslationOptions(TranslationOptions):
    fields = ('title',)

