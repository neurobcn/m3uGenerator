import  requests
from m3uservers.forms import server1
from m3uservers.models import listservers
from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.
def home_view(request):
    return render(request, 'home.html') # HttpResponse("<h1>Hello World</h1>") # string of HTML code

def uploadM3U(request):
    context = {
        'list1': server1(),
    }
    return render(request, 'upload.html', context)

def updateM3U(request, id):
    server = listservers.objects.get(id=id)
    form = server1(instance=server)
    url = server.ipNameServer
    try:
        r = requests.get(url)
        r = r.text
    except Exception as ex:
        r = str(ex)

    
    if request.method == 'POST':
        form = server1(request.POST, instance=server)
        server.contentm3u2 = r
        print('***************************************')
        print(form)
        print('***************************************')

        if form.is_valid():
            form.save()
            return redirect('home')    

    context = {
        'list1': server,
        'url': url,
        'm3u': r,
    }
    return render(request, 'update.html', context)


def listM3U(request):
    servers = listservers.objects.all()
    url = servers[1].ipNameServer
    
    #print ('url:' + url)
    #r = requests.get(url)
    #servers[0].contentm3u = r.text
    #print(r.text)

    context = {
        'list2': servers,
        #'m3u': r.text,
    }

    return render(request, 'm3uList.html', context)
 