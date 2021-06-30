from django.shortcuts import render
#from .forms import serverForm, ImageForm
from .models import listservers, Images
# Create your views here.

def ind(request):
    return render(request, 'upload.html')