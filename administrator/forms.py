from django.forms import ModelForm,TextInput, Select
from . import models
from bootstrap_modal_forms.forms import BSModalModelForm


class ItemForm(BSModalModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Enter Name',
                }
            ),
            'description': TextInput(
                attrs={
                    'placeholder': 'Enter Description',
                }
            ),
            'category': Select(
                attrs={
                    'style': 'width:100%;'
                }
            ),
            'department': TextInput(
                attrs={
                    'placeholder': 'Enter Department',
                }
            ),

        }


class BannerForm(BSModalModelForm):
    class Meta:
        model = models.Banner
        fields = '__all__'
        enctype = "multipart/form-data"
        ISMAIN = ((True, 'Yes'), (False, 'No'),)
        BUTTONALIGN = (('Center','center'),('Left','left'),('Right','right'))
        widgets = {
            'header': TextInput(
                attrs={
                    'placeholder': 'Enter Header',
                }
            ),
            'caption': TextInput(
                attrs={
                    'placeholder': 'Enter Banner Caption',
                }
            ),
            'season':Select(
                attrs={
                    'style': 'width:100%;'
                }
            ),
            'isMain':Select(
                attrs={
                    'style': 'width:100%;border:none'
                },
                choices=ISMAIN
            ),
            'buttonAlign':Select(
                attrs={
                    'style': 'width:100%;border:none'
                },
                choices=BUTTONALIGN
            )
        }


class CsvForm(ModelForm):
    class Meta:
        model = models.Csv
        fields = ('file_name',)
