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
        # widgets = {
        #     'checkedForOutput': widgets.CheckboxInput,
        # }

class editCanalForm(forms.Form):
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
