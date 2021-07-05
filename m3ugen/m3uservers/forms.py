from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import listservers
from .models import canal


class newServerForm(forms.ModelForm): # Форма для добавления плейлиста
    class Meta:
        model = listservers
        fields = ('urlServer', 'nameServer')

class listServerForm(forms.ModelForm):
    class Meta:
        model = listservers
        fields = '__all__'

class listCanalForm(forms.ModelForm):
    class Meta:
        model = canal
        fields = '__all__'
        widgets = {
            'checkedForOutput': widgets.CheckboxInput,
        }

class editCanalForm(forms.ModelForm):
    checkedForOutput = forms.BooleanField(label='', required=False)
    nameGroup = forms.CharField(label='', required=False)
    class Meta:
        model = canal
        exclude = ['idm3u', 'idCanal', 'nameCanal', 'urlCanal']
 

# class canals2 (forms.ModelForm):
#     class Meta:
#         model = listCanalForm
#         fields = '__all__'
