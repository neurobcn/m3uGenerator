import  requests
from m3uservers.forms import ImageForm, server1
from m3uservers.models import listservers
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_view(request):
    #return HttpResponse("<h1>Hello World</h1>") # string of HTML code
    # context = [

    # ]
    return render(request, 'home.html') # HttpResponse("<h1>Hello World</h1>") # string of HTML code

def uploadM3U(request):
    context = {
        'form': ImageForm(),
        'list1': server1(),
    }
    return render(request, 'upload.html', context)


def listM3U(request):
    servers = listservers.objects.all()
    context = {
        'list2': servers,
    }
    url = servers[0].ipNameServer
        
    # fp = urllib.request.urlopen("http://www.python.org")
    # mybytes = fp.read()

    # mystr = mybytes.decode("utf8")
    # fp.close()
    # print(mystr)
    
    print ('url:' + url)
    http=''
    # if 'http' in url:
    #     http = urllib.request.urlopen(url)
    #     mybytes = http.read()
    #     mystr = mybytes.decode("utf8")
    #     http.close()
    r = requests.get(url)
    print(r.text)

    return render(request, 'm3uList.html', context)
 