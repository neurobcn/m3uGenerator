from django.db import models
from django.db.models import fields
from m3ugen.settings import STATIC_URL
import  requests
from m3uservers.forms import newServerForm, listServerForm, listCanalForm
from m3uservers.models import listservers, canal
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.conf import settings


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
                    'error': 'Ошибка:'+ m3u # Сообщение об ошибке
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
    return redirect('updateM3U2', id)


def updateM3U2(request, id): # Управление каналами
    # 
    form = listCanalForm(request.POST)
    if request.method == 'POST': # Если обновляем
        form = listCanalForm(request.POST) # Заполняем форму
        print('form:', form)
        if form.is_valid():
            #sss = form.cleaned_data('')
            print('form:', form)
    #

    canalList = canal.objects.filter(idm3u=id).order_by('idCanal') # список каналов
    countAll = canal.objects.filter(idm3u=id).count() # Количество каналов в списке
    countChecked = canal.objects.filter(idm3u=id, checkedForOutput = True).count() # количество отмеченных каналов
    serverList = listservers.objects.filter(idServer=id) # текущий сервер
    context = {
        'serverList': serverList,
        'countChecked': countChecked,
        'countAll': countAll, 
        'canalList': canalList,
        #'form': form,
    }
    return render(request, 'update2.html', context)

def updateM3U(request, id):

    #cans = canals2.objects.

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


def listM3U(request): # Список исходных плейлистов
    serverList = listservers.objects.all()
    #form = listServerForm()
    context = {
        'serverList': serverList,
    #   'form': form,
    }
    return render(request, 'm3uList.html', context)

def generateM3U(): # Генерируем файл M3U
    # Выбираем все помеченые каналы
    canals = canal.objects.filter(checkedForOutput = True).order_by('idm3u', 'idCanal')
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
    fileName = "./static/myList.m3u"
    try:
        with open(fileName, 'w', encoding='utf-8') as f: # Запись в файл
            f.write(outputstring)
    except BaseException as ex:
        fileName='Ошибка записи в файл:' + ex
    return fileName




