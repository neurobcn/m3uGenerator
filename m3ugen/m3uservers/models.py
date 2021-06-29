from django.db import models
from django.db.models.base import Model

# Create your models here.
class listservers(models.Model):
    idServer = models.DecimalField(max_digits=3, decimal_places=0)
    nameServer = models.CharField(max_length=1024)
    ipNameServer = models.CharField(max_length=255)
    addressServer = models.CharField(max_length=1024)
    contentm3u2 = models.CharField(max_length=50000, default='')


class Images(models.Model):
    image = models.ImageField(upload_to='images/')
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

class canal(models.Model):
    idm3u = models.DecimalField(max_digits=3, decimal_places=0)
    idCanal = models.DecimalField(max_digits=10, decimal_places=0)
    nameCanal = models.CharField(max_length=1024)
    nameGroup = models.CharField(max_length=1024)
    urlCanal = models.CharField(max_length=1024)
