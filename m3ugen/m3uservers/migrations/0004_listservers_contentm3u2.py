# Generated by Django 3.2.4 on 2021-06-27 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('m3uservers', '0003_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='listservers',
            name='contentm3u2',
            field=models.CharField(default='', max_length=50000),
        ),
    ]