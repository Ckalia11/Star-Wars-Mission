from django import forms
from django.forms import ValidationError


class UploadJsonFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

# def clean_empire_file(self):
#     allowed_file_extensions = ('.json')
#     empire_file = self.cleaned_data.get('file')
#     if not empire_file:
#         raise ValidationError('Please upload the empire file')
#     name, ext = os.path.splitext(empire_file.name)
#     if ext not in allowed_file_extensions:
#         raise ValidationError('File must be of type .json')
#     return empire_file