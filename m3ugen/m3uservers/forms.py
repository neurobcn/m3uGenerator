from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import ListServers
from .models import Canal


class NewServerForm(forms.ModelForm): # Форма для добавления плейлиста
    class Meta:
        model = ListServers
        fields = ('urlServer', 'nameServer')

class ListServerForm(forms.ModelForm):
    class Meta:
        model = ListServers
        fields = '__all__'

class ListCanalForm(forms.ModelForm):
    class Meta:
        model = Canal
        fields = '__all__'
        # widgets = {
        #     'checkedForOutput': widgets.CheckboxInput,
        # }

class EditCanalForm(forms.Form):
    idm3u = forms.IntegerField(label='', required=False, disabled=True)
    idCanal = forms.IntegerField(label='', required=False, disabled=True)
    nameCanal = forms.CharField(label='', required=False, disabled=True)
    nameGroup = forms.CharField(label='', required=False)
    urlCanal = forms.CharField(label='', required=False, disabled=True)
    checkedForOutput = forms.BooleanField(label='', required=False)
    widgets = {
        'checkedForOutput': widgets.CheckboxInput,
    }

     

# class canals2 (forms.ModelForm):
#     class Meta:
#         model = listCanalForm
#         fields = '__all__'
