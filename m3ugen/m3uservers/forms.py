from django import forms
from .models import listservers
from .models import Images


class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('image',)

class newServerForm(forms.ModelForm):
    class Meta:
        model = listservers
        fields = ('urlServer', 'nameServer')


# class UpdateProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['picture', 'phone', 'description']        