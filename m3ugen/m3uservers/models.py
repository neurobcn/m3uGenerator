from django.db import models

# Create your models here.
class listservers(models.Model):
    idServer = models.DecimalField(max_digits=3, decimal_places=0)
    nameServer = models.CharField(max_length=1024)
    ipNameServer = models.CharField(max_length=255)
    addressServer = models.CharField(max_length=1024)
    contentm3u = models.TextField(null=True, blank=True)


class Images(models.Model):
    image = models.ImageField(upload_to='images/')
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

