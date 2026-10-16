from django import forms

from contacts.models import ContactForm


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ('first_name', 'last_name', 'phone_number', 'email',
                  'contact_form', 'text')

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            # в шаблоне поле темы называется "select", пустое значение = "Другое"
            data['contact_form'] = data.get('select') or 'other'
        super().__init__(data, *args, **kwargs)
