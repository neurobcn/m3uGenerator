from django.db import models
from django.db.models.base import Model


# Create your models here.
class listservers(models.Model):
    idServer = models.IntegerField()
    nameServer = models.CharField(max_length=1024)
    urlServer = models.CharField(max_length=1024)
    contentm3u2 = models.CharField(max_length=50000, default='')

class canal(models.Model):
    idm3u = models.IntegerField()
    idCanal = models.IntegerField()
    nameCanal = models.CharField(max_length=1024)
    nameGroup = models.CharField(max_length=1024)
    urlCanal = models.CharField(max_length=1024)
    checkedForOutput = models.BooleanField(default=True) # флаг выбора для выходного файла

class groups(models.Model):
    nameGroup = models.CharField(max_length=50)

# class allCanal(canal):
#     pass
