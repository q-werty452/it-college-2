from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from contacts.models import Contacts, Department, ContactForm, SocialLink
from core.admin_mixins import SingletonAdminMixin, ReadOnlySubmissionAdminMixin



@admin.register(Contacts)
class ContactsAdmin(SingletonAdminMixin, TranslationAdmin):
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
class ContactFormAdmin(ReadOnlySubmissionAdminMixin, admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'phone_number', 'email', 'contact_form', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'contact_form', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email', 'text')
    date_hierarchy = 'created_at'



@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active')
    list_editable = ('is_active',)

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
                'css/icon-picker.css',
            )
        }
        js = ('js/icon-picker.js',)
