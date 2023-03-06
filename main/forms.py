from .models import Functions
from django.forms import ModelForm, TextInput, Textarea, FileInput


class FunctionsForm(ModelForm):
    class Meta:
        model = Functions
        fields = ["name", "about"]
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название функции'
            }),
            "about": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание функции'
            }),
            # "func": FileInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Введите функцию'
            # })
        }
