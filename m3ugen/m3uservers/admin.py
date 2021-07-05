from django.contrib import admin

# Register your models here.
from .models import Canal, ListServers
# Регистрируем на админ панели наши продукты
admin.site.register(ListServers)
admin.site.register(Canal)