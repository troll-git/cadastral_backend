# Generated by Django 3.1.1 on 2020-09-26 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polyserver_api', '0003_auto_20200926_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pozwolenia',
            name='imie_inwestora',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='pozwolenia',
            name='nazwa_inwestor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pozwolenia',
            name='nazwisko_inwestora',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
