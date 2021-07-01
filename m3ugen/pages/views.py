import  requests
from m3uservers.forms import newServerForm, listServerForm, listCanalForm
from m3uservers.models import listservers, canal
from django.shortcuts import redirect, render
from django.http import HttpResponse

def downloadm3u(url):
    try:
        m3u = requests.get(url)
        m3u = m3u.text
    except Exception as ex:
        m3u = 'Invalid URL:' + str(ex)
    return m3u


# Create your views here.
def home_view(request):
    return render(request, 'home.html')

def uploadM3U(request):
    if request.method == 'POST': # Если обновляем
        form = newServerForm(request.POST) # Заполняем форму
        if form.is_valid(): # Если поля заполнены
            maxId = listservers.objects.latest('idServer').idServer # получаем последний добавленый idServer
            post = form.save(commit=False) # Сохранеям форму без записи в БД
            post.idServer = maxId + 1 # Новый idServer
            url = post.urlServer # из формы вытягиваем URL
            m3u = downloadm3u(url) # и скачиваем по ссылке
            if 'Invalid URL' in m3u: # Если ошибка 
                context = { # подготавливаем форму для нового ввода
                    'form': form,
                    'error': m3u # Сообщение об ошибке
                }
                return render(request, 'upload.html', context)
            post.contentm3u2 = m3u  # Если ошибок нет, 
            post.save()             # сохраняем полученное в базу
            return redirect('listM3U') # и переходим на список источников
    else:
        form = newServerForm() # если только открыли пустая форма
        context = { 
            'form': form,
        }
    return render(request, 'upload.html', context)

def deleteM3U(request, id): # Удаляем сервер из списка
    m3u = listservers.objects.get(idServer=id) 
    m3u.delete()
    return redirect('listM3U')

def reloadList(request, id):
    pass

def updateM3Udb(request, id): # Обновление списка каналов из сохраненного в базе contentm3u2
    server = listservers.objects.get(idServer=id) # Выбираем сервер
    content = server.contentm3u2 # Вытягиваем сохраненный content

    canals = content.split('#EXTINF:') # разбиваем на каналы - разделитель EXTINF
    i=1
    canals.pop(0) # вырезаем первую строку
    for can in canals: # Пробегаем по списку
        items = can.splitlines() # разбиваем на элементы
        print('stttt:', items)
        
        title = items[0][items[0].find(',')+1:].strip() # Заголовок
        grp = ''
        url = ''

        if '#EXTGRP:' in items[1]: # во второй строке может быть Группа
            grp=items[1].replace('#EXTGRP:','') # если так, то сохраняем
            url = items[2] # далее ссылка на поток
        else:
            url = items[1] # ссылка на поток

        # print('title:' + title + '|grp:' + grp + '|url:' + url)

        try: # Проверяем есть ли такой канал в базе
            can = canal.objects.get(nameCanal=title, urlCanal=url, idm3u=id)
        except canal.DoesNotExist: # если канала нет в базе, добавляем
            can = canal(nameCanal=title, urlCanal=url, nameGroup=grp, idm3u=id, idCanal = i)
            can.save()
        i += 1
    return redirect('listM3U')


def updateM3U2(request, id):

    form = listCanalForm(request.POST)
    if request.method == 'POST': # Если обновляем
        form = listCanalForm(request.POST) # Заполняем форму
        print('form:', form)
        if form.is_valid():
            #sss = form.cleaned_data('')
            print('form:', form)
    cannals = canal.objects.filter(idm3u=id).order_by('idCanal')
    countAll = canal.objects.filter(idm3u=id).count()
    countChecked = canal.objects.filter(idm3u=id, checkedForOutput = True).count()
    serv1 = listservers.objects.filter(idServer=id)
    context = {
        'list1': serv1,
        'countChecked': countChecked,
        'countAll': countAll, 
        'list2': cannals,
        'form':form,
    }
    return render(request, 'update2.html', context)


def updateM3U(request, id):
    # server = listservers.objects.get(idServer=id)
    # #form = server1(instance=server)
    # url = server.urlServer
    # r = server.contentm3u2
    # #r=downloadm3u(url)

    # r1=r.split('#EXTINF:')
    # i=0
    # LL=[]

    # for str1 in r1:

    #     #print(str(i) +':' + str1)
    #     str2=str1.replace(chr(10),"").replace(chr(13),"").replace("#EXTINF:", "\n#EXTINF:").replace("#EXTGRP:", ", GRP:")
    #     t = str2[str2.find(','):]
    #     #print('str2:'+str2)
    #     #print('t:'+t)
    #     s1=''
    #     if 'http://'  in t:
    #         s1='http://'
    #     if 'https://' in t:
    #         s1='https://'
    #     if 'rtmp://'  in t:
    #         s1='rtmp://'
    #     if 'udp://'   in t: 
    #         s1='udp://'
    #     #print('s1_1:'+ s1)
    #     try:
    #         url=t[t.find(s1):]
    #         #print('url:' + url)
    #         grp=''
    #         if 'GRP:' in str2:
    #             grp = str2[str2.find('GRP:')+4:str2.find(s1)].strip()
    #             s1=', GRP:'
    #         #print('grp:'+ grp)
    #         #print('s1:' + s1)
    #         tmp = str2[:str2.rfind(s1)]
    #         #print('tmp:' + tmp)
    #         title=tmp[tmp.rfind(',')+1:].strip()
    #         #print('title:'+ title)
    #         logo = ''
    #         #LL.append({'url':url, 'img':logo, 'title':title, 'group': grp })

    #         try: # 
    #             can = canal.objects.get(nameCanal=title, urlCanal=url, idm3u=id)
    #         except canal.DoesNotExist: # если канала нет в базе, добавляем
    #             can = canal(nameCanal=title, urlCanal=url, nameGroup=grp, idm3u=id, idCanal = i)
    #             can.save()
    #     except:
    #         pass
        

    #     i += 1
    
    #print('LL:******************************')
    #print(LL)
    #print('server**************')
    #print(server)
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
    

    cannals = canal.objects.filter(idm3u=id).order_by('idCanal')
    countAll = canal.objects.filter(idm3u=id).count()
    countChecked = canal.objects.filter(idm3u=id, checkedForOutput = True).count()
    serv1 = listservers.objects.filter(idServer=id)
    context = {
        'list1': serv1,
        'countChecked': countChecked,
        'countAll': countAll, 
        'list2': cannals,
    }
    return render(request, 'update.html', context)


def listM3U(request):
    servers = listservers.objects.all()
    
    context = {
        'list2': servers,
    }

    return render(request, 'm3uList.html', context)

