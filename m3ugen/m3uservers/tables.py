import django_tables2 as tables
from .models import canal

class PersonTable(tables.Table):
    class Meta:
        model = canal
        template_name = "django_tables2/bootstrap.html"
        fields = ("idCanal", "nameCanal", "nameGroup", "checkedForOutput")