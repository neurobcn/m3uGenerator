from django import forms
from .models import listservers
from .models import Images


class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('image',)

class server1(forms.ModelForm):
    class Meta:
        model = listservers
        fields = ('nameServer',)