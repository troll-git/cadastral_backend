# Generated by Django 3.1.1 on 2020-10-02 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polyserver_api', '0028_auto_20201002_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pozwolenia',
            name='identyfikator',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pozwolenia',
            name='numer_dzialki',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pozwolenia',
            name='obreb_numer',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pozwoleniageom',
            name='identyfikator',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pozwoleniageom',
            name='numer_dzialki',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pozwoleniageom',
            name='obreb_numer',
            field=models.CharField(max_length=50, null=True),
        ),
    ]