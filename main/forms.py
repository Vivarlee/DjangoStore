from .models import Item
from django.forms import ModelForm, TextInput, Textarea, FileInput


class ItemsForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "price", "about", "image"]
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите наименование товара'
            }),
            "price": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цену товара'
            }),
            "about": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание товара'
            }),
            "image": FileInput(attrs={

            })
        }
