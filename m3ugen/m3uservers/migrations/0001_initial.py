# Generated by Django 3.2.4 on 2021-06-26 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='listservers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameServer', models.CharField(max_length=1024)),
                ('ipNameServer', models.CharField(max_length=255)),
                ('addressServer', models.CharField(max_length=1024)),
            ],
        ),
    ]