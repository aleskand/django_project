from django import forms
from .models import Annotation

class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation
        fields = ['sort', 'value', 'author']
        labels = {
            'sort': 'Type',
            'value': 'Annotation Value',
            'author': 'Author',
            'an_date': 'Annotation Date',
            'snp': 'Associated SNP'
        }
        widgets = {
            'an_date': forms.HiddenInput(),
            'snp': forms.HiddenInput()
        }
