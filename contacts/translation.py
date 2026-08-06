from contacts.models import Contacts, Department
from modeltranslation.translator import register, TranslationOptions



@register(Contacts)
class ContactsTranslationOptions(TranslationOptions):
    fields = ('address','work_hours',)



@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name','work_hours',)
