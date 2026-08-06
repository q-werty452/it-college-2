from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from contacts.models import Contacts, Department, ContactForm, SocialLink



@admin.register(Contacts)
class ContactsAdmin(TranslationAdmin):
    list_display = (
        'email',
        'phone_admission',
        'phone_students',
        'telegram',
        'instagram',
        'work_hours',
    )



@admin.register(Department)
class DepartmentAdmin(TranslationAdmin):
    list_display = (
        'name', 'phone_number', 'email', 'work_hours',
    )

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
                'css/icon-picker.css',
            )
        }
        js = ('js/icon-picker.js',)



@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'created_at',)



@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
                'css/icon-picker.css',
            )
        }
        js = ('js/icon-picker.js',)
