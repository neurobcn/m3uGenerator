import  requests
from m3uservers.forms import ImageForm, server1
from m3uservers.models import listservers
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_view(request):
    return render(request, 'home.html') # HttpResponse("<h1>Hello World</h1>") # string of HTML code

def uploadM3U(request):
    context = {
        'form': ImageForm(),
        'list1': server1(),
    }
    return render(request, 'upload.html', context)

def updateM3U(request, id):
    server = listservers.objects.get(id=id)
    url = server.ipNameServer
    r = requests.get(url)

    context = {
        'list1': server,
        'url': url,
        'm3u': r.text,
    }
    return render(request, 'update.html', context)


def listM3U(request):
    servers = listservers.objects.all()
    url = servers[1].ipNameServer
    
    print ('url:' + url)
    r = requests.get(url)
    #servers[0].contentm3u = r.text
    print(r.text)

    context = {
        'list2': servers,
        'm3u': r.text,
    }

    return render(request, 'm3uList.html', context)
 