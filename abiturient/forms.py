from django import forms
from django.core.exceptions import ValidationError

from abiturient.models import SubmitDocument

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 МБ


class SubmitDocumentForm(forms.ModelForm):
    class Meta:
        model = SubmitDocument
        fields = (
            'first_name', 'last_name', 'middle_name', 'phone', 'email',
            'birth_date', 'address', 'citizenship',
            'program', 'form_of_study', 'study_form', 'source', 'comment',
            'passport', 'education_document', 'photo', 'medical_certificate',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['program'].required = True
        self.fields['program'].queryset = self.fields['program'].queryset.filter(is_active=True)

    def _clean_file(self, name):
        file = self.cleaned_data.get(name)
        if file and file.size > MAX_UPLOAD_SIZE:
            raise ValidationError('Файл больше 10 МБ.')
        return file

    def clean_passport(self):
        return self._clean_file('passport')

    def clean_education_document(self):
        return self._clean_file('education_document')

    def clean_photo(self):
        return self._clean_file('photo')

    def clean_medical_certificate(self):
        return self._clean_file('medical_certificate')

