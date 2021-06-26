from django.db import models

# Create your models here.
class listservers(models.Model):
    nameServer = models.CharField(max_length=1024)
    ipNameServer = models.CharField(max_length=255)
    addressServer = models.CharField(max_length=1024)

