from django.db import models
from django.db.models import fields
from m3ugen.settings import STATIC_URL
import  requests
from m3uservers.forms import NewServerForm, ListServerForm, ListCanalForm, EditCanalForm
from m3uservers.models import ListServers, Canal
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.conf import settings
from django.forms import formset_factory
from django.forms import modelformset_factory

def downloadm3u(url): # Загрузка m3u 
    try:
        m3u = requests.get(url) # Пробуем загрузить
        m3u = m3u.text # если все норм сохраняем как текст
    except Exception as ex: # если не получилось
        m3u = 'Invalid URL:' + str(ex) # Сообщаем об ошибке
    return m3u

def home_view(request):
    url = generateM3U() # Генерируем выходной файл
    if 'Ошибка' in url: # Если ошибка 
        context = {
            'error': 'Ошибка:'+ url # Сообщение об ошибке
        }    
    else:
        context = { # если нет ошибок показываем кнопку с ссылкой
            'url':url,
            'STATIC_URL':STATIC_URL,
        }
    return render(request, 'home.html', context)

def uploadM3U(request):
    if request.method == 'POST': # Если обновляем
        form = NewServerForm(request.POST) # Заполняем форму
        if form.is_valid(): # Если поля заполнены
            maxId = ListServers.objects.latest('idServer').idServer # получаем последний добавленый idServer
            post = form.save(commit=False) # Сохранеям форму без записи в БД
            post.idServer = maxId + 1 # Новый idServer
            url = post.urlServer # из формы вытягиваем URL
            m3u = downloadm3u(url) # и скачиваем по ссылке
            if 'Invalid URL' in m3u: # Если ошибка 
                context = { # подготавливаем форму для нового ввода
                    'form': form,
                    'error': 'Ошибка:'+ m3u # Сообщение об ошибке
                }
                return render(request, 'upload.html', context)
            post.contentm3u2 = m3u  # Если ошибок нет, 
            post.save()             # сохраняем полученное в базу
            return redirect('listM3U') # и переходим на список источников
    else:
        form = NewServerForm() # если только открыли пустая форма
        context = { 
            'form': form,
        }
    return render(request, 'upload.html', context)

def deleteM3U(request, id): # Удаляем сервер из списка
    m3u = ListServers.objects.get(idServer=id)
    canals = Canal.objects.filter(idm3u=id)
    canals.delete()
    m3u.delete()
    return redirect('listM3U')

def reloadList(request, id):
    pass

def reloadList(request, id): # Обновление списка каналов из сохраненного в базе contentm3u2
    server = ListServers.objects.get(idServer=id) # Выбираем сервер
    
    url = server.urlServer # Ссылка на источник
    m3u = downloadm3u(url) # скачиваем список каналов из источника
    if 'Invalid URL' not in m3u: # Если ошибок нет - 
        server.contentm3u2 = m3u # то полученный контент
        server.save()            # сохраняем в базу

    content = server.contentm3u2 # Вытягиваем сохраненный content

    deleteList = Canal.objects.filter(idm3u=id) # Подготавливаем и 
    deleteList.delete()                         # очищаем список каналов в базе

    canals = content.split('#EXTINF:') # разбиваем на каналы - разделитель EXTINF
    i=1
    canals.pop(0) # вырезаем первую строку 
    for can in canals: # Пробегаем по списку
        try: # Если в описании канала ошибка, пропускаем (временно - ошибку в консоль)
            items = can.splitlines() # разбиваем на элементы

            title = items[0][items[0].rfind(',')+1:] # Заголовок
            grp = ''
            url = ''

            if '#EXTGRP:' in items[1]: # во второй строке может быть Группа
                grp=items[1].replace('#EXTGRP:','').strip() # если так, то сохраняем
                url = items[2].strip() # далее ссылка на поток
            else:
                url = items[1].strip() # ссылка на поток

            try: # Проверяем есть ли такой канал в базе
                can = Canal.objects.get(nameCanal=title, urlCanal=url, idm3u=id)
            except Canal.DoesNotExist: # если канала нет в базе, добавляем
                can = Canal(nameCanal=title, urlCanal=url, nameGroup=grp, idm3u=id, idCanal = i)
                can.save()
        except BaseException as ex:
            print('error:',str(i),':',ex)
        i += 1
    return redirect('updateList', id)


def updateList(request, id): # Управление каналами
    canalList = Canal.objects.filter(idm3u=id).order_by('idCanal') # список каналов
    countAll = Canal.objects.filter(idm3u=id).count() # Количество каналов в списке
    countChecked = Canal.objects.filter(idm3u=id, checkedForOutput = True).count() # количество отмеченных каналов
    serverList = ListServers.objects.filter(idServer=id) # текущий сервер
    context = {
        'serverList': serverList,
        'countChecked': countChecked,
        'countAll': countAll, 
        'canalList': canalList,
    }
    return render(request, 'updateList.html', context)

def updateCanal(request, idm3u, idcanal):
    can = Canal.objects.get(idm3u = idm3u, idCanal = idcanal)
    if request.method == 'POST':
        check_status = True if request.POST['checked'] == 'true' else False
        can.checkedForOutput = check_status
        can.save()
        return HttpResponse("")

def listM3U(request): # Список исходных плейлистов
    serversList = ListServers.objects.all()
    serverList=[]
    for server in serversList:
        countAll = Canal.objects.filter(idm3u=server.idServer).count() # Количество каналов в списке
        countChecked = Canal.objects.filter(idm3u=server.idServer, checkedForOutput = True).count() # количество отмеченных каналов

        serverList.append([server.idServer,
                           server.nameServer,
                           server.urlServer,
                           countChecked,
                           countAll
                        ])

    context = {
        'serverList': serverList,
    
    }
    return render(request, 'm3uList.html', context)

def generateM3U(): # Генерируем файл M3U
    # Выбираем все помеченые каналы
    canals = Canal.objects.filter(checkedForOutput = True).order_by('idm3u', 'idCanal')
    listOut=[] # Выходной list
    # первая строка - заголовок с сылкой на EPG
    listOut.append('#EXTM3U url-tvg="http://www.teleguide.info/download/new3/jtv.zip"')
    for can in canals: # Пробегаем по всем каналам
        listOut.append('#EXTINF:-1,'+ can.nameCanal) # Строка заголовка
        if can.nameGroup: # если есть название группы
            listOut.append('#EXTGRP:' + can.nameGroup) # то следущая строка - Группа
        listOut.append(can.urlCanal) # далее ссылка на канал
    #print(listOut)
    outputstring='\n'.join(listOut) # итоговый список выводим через разделитель строк "\n" 
    fileName = "myList.m3u"
    try:
        with open(fileName, 'w', encoding='utf-8') as f: # Запись в файл
            f.write(outputstring)
    except BaseException as ex:
        fileName='Ошибка записи в файл:' + ex
    return fileName

def playLink(request, idm3u, idCanal):
    m3ulink = Canal.objects.get(idm3u=idm3u, idCanal=idCanal).urlCanal
    content = {
        'm3ulink': m3ulink,
    }
    return render(request, 'playlink.html', content)