# Generated by Django 3.2.4 on 2021-07-05 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('m3uservers', '0009_canal_checkedforoutput'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameGroup', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Images',
        ),
    ]