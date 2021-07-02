from django import forms
from django.db.models import fields
from .models import listservers
from .models import canal
#from django.forms.models import BaseInlineFormSet #, inlineformset_factory

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
 
# class BaseChildrenFormset(BaseInlineFormSet):
#     pass

# canals = inlineformset_factory( canal,
#                                 formset=BaseChildrenFormset,
#                                 extra=1)

# class canals2 (forms.ModelForm):
#     class Meta:
#         model = listCanalForm
#         fields = '__all__'


# class UpdateProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['picture', 'phone', 'description']        