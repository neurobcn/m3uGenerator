from django.contrib import admin

# Register your models here.
from .models import canal, listservers
# Регистрируем на админ панели наши продукты
admin.site.register(listservers)
admin.site.register(canal)