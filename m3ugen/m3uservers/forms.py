from django import forms
from .models import listservers
from .models import canal


class newServerForm(forms.ModelForm):
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


# class UpdateProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['picture', 'phone', 'description']        