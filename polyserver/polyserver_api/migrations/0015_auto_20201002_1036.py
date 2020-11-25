# Generated by Django 3.1.1 on 2020-10-02 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polyserver_api', '0014_auto_20201002_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pozwolenia',
            name='jednostka_numer_ew',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='pozwolenia',
            name='kategoria',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='pozwolenia',
            name='nr_domu',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='pozwolenia',
            name='numer_arkusza_dzialki',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='pozwolenia',
            name='numer_dzialki',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='pozwolenia',
            name='obreb_numer',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='pozwolenia',
            name='terc',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='pozwoleniageom',
            name='jednostka_numer_ew',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='pozwoleniageom',
            name='kategoria',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='pozwoleniageom',
            name='nr_domu',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='pozwoleniageom',
            name='numer_arkusza_dzialki',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='pozwoleniageom',
            name='numer_dzialki',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='pozwoleniageom',
            name='obreb_numer',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='pozwoleniageom',
            name='terc',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
