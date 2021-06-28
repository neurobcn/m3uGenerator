import  requests
from m3uservers.forms import server1
from m3uservers.models import listservers, canal
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


    try:
        obj = canal.objects.get(nameCanal='John', urlCanal='Lennon')
    except canal.DoesNotExist:
        obj = canal(nameCanal='John', urlCanal='Lennon', nameGroup='other', idm3u=999, idCanal = 1)
        obj.save()

    r1=r.split('#EXTINF:')
    i=0
    LL=[]

    for str1 in r1:

        print(str(i) +':' + str1)
        str2=str1.replace(chr(10),"").replace(chr(13),"").replace("#EXTINF:", "\n#EXTINF:").replace("#EXTGRP:", ", GRP:")
        t = str2[str2.rfind(','):]
        if 'http://'  in t:
            s1='http://'
        if 'https://' in t:
            s1='https://'
        if 'rtmp://'  in t:
            s1='rtmp://'
        if 'udp://'   in t: 
            s1='udp://'
        try:
            url=t[t.find(s1):]
            print('url:' + url)
            grp=''
            if 'GRP:' in str2:
                grp = str2[str2.find('GRP:')+4:str2.find(s1)].strip()
                s1=', GRP:'
            print('grp:'+ grp)
            print('s1:' + s1)
            tmp = str2[:str2.rfind(s1)]
            print('tmp:' + tmp)
            title=tmp[tmp.rfind(',')+1:].strip()
            print('title:'+ title)
            logo = ''
            LL.append({'url':url, 'img':logo, 'title':title, 'group': grp })

            try: # 
                can = canal.objects.get(nameCanal=title, urlCanal=url)
            except canal.DoesNotExist: #if nameCanal does not exist? create it
                can = canal(nameCanal=title, urlCanal=url, nameGroup=grp, idm3u=id, idCanal = i)
                can.save()
        except:
            pass
        

        i += 1
    
    print('LL:******************************')
    print(LL)
    #r1 = r.replace(chr(10),"").replace(chr(13),"").replace("#EXTINF:", "\n#EXTINF:").replace("#EXTGRP:", ", GRP:")
        
    # if request.method == 'POST':
    #     form = server1(request.POST, instance=server)
    #     server.contentm3u2 = r
    #     print('***************************************')
    #     print(form)
    #     print('***************************************')

    #     if form.is_valid():
    #         form.save()
    #         return redirect('home')    

    context = {
        'list1': server,
        'url': url,
        'm3u': r,
        'r1': r1,
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
 