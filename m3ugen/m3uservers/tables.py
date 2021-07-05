import django_tables2 as tables
from .models import Canal

class PersonTable(tables.Table):
    class Meta:
        model = Canal
        template_name = "django_tables2/bootstrap.html"
        fields = ("idCanal", "nameCanal", "nameGroup", "checkedForOutput")