# Generated by Django 3.1.2 on 2020-11-12 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polyserver_api', '0048_auto_20201109_2122'),
    ]

    operations = [
        migrations.CreateModel(
            name='PozwoleniaUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numer_urzad', models.CharField(max_length=50)),
                ('nazwa_organu', models.CharField(max_length=50)),
                ('adres_organu', models.CharField(max_length=50)),
                ('data_wplywu_wniosku', models.DateField()),
                ('numer_decyzji_urzedu', models.CharField(max_length=50)),
                ('data_wydania_decyzji', models.DateField()),
                ('nazwisko_inwestora', models.CharField(blank=True, max_length=50, null=True)),
                ('imie_inwestora', models.CharField(blank=True, max_length=50, null=True)),
                ('nazwa_inwestor', models.CharField(blank=True, max_length=10000, null=True)),
                ('wojewodztwo', models.CharField(max_length=50)),
                ('miasto', models.CharField(max_length=50, null=True)),
                ('terc', models.CharField(blank=True, max_length=50, null=True)),
                ('cecha', models.CharField(blank=True, max_length=5, null=True)),
                ('ulica', models.CharField(blank=True, max_length=50, null=True)),
                ('ulica_dalej', models.CharField(blank=True, max_length=50, null=True)),
                ('nr_domu', models.CharField(blank=True, max_length=50, null=True)),
                ('rodzaj_inwestycji', models.CharField(max_length=512, null=True)),
                ('kategoria', models.CharField(max_length=10, null=True)),
                ('nazwa_zamierzenia_bud', models.CharField(max_length=512, null=True)),
                ('nazwa_zam_budowlanego', models.CharField(max_length=10000, null=True)),
                ('kubatura', models.FloatField(blank=True, null=True)),
                ('projektant_nazwisko', models.CharField(blank=True, max_length=50, null=True)),
                ('projektant_imie', models.CharField(blank=True, max_length=50, null=True)),
                ('projektant_numer_uprawnien', models.CharField(blank=True, max_length=200, null=True)),
                ('jednostka_numer_ew', models.CharField(max_length=50, null=True)),
                ('obreb_numer', models.CharField(max_length=50, null=True)),
                ('numer_dzialki', models.CharField(max_length=50, null=True)),
                ('identyfikator', models.CharField(max_length=50, null=True)),
                ('numer_arkusza_dzialki', models.CharField(blank=True, max_length=50, null=True)),
                ('jednostka_stara_numeracja_z_wniosku', models.CharField(blank=True, max_length=50, null=True)),
                ('stara_numeracja_obreb_z_wniosku', models.CharField(blank=True, max_length=50, null=True)),
                ('stara_numeracja_dzialka_z_wniosku', models.CharField(blank=True, max_length=4000, null=True)),
                ('created_at', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WnioskiUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numer_ewidencyjny_system', models.CharField(max_length=50)),
                ('numer_ewidencyjny_urzad', models.CharField(max_length=50)),
                ('data_wplywu_wniosku_do_urzedu', models.DateField()),
                ('nazwa_organu', models.CharField(max_length=50)),
                ('wojewodztwo_objekt', models.CharField(max_length=50)),
                ('obiekt_kod_pocztowy', models.CharField(blank=True, max_length=50, null=True)),
                ('miasto', models.CharField(max_length=50, null=True)),
                ('terc', models.CharField(blank=True, max_length=50, null=True)),
                ('cecha', models.CharField(blank=True, max_length=5, null=True)),
                ('ulica', models.CharField(blank=True, max_length=50, null=True)),
                ('ulica_dalej', models.CharField(blank=True, max_length=50, null=True)),
                ('nr_domu', models.CharField(blank=True, max_length=50, null=True)),
                ('kategoria', models.CharField(max_length=10, null=True)),
                ('nazwa_zam_budowlanego', models.CharField(max_length=512, null=True)),
                ('rodzaj_zam_budowlanego', models.CharField(max_length=10000, null=True)),
                ('kubatura', models.FloatField(blank=True, null=True)),
                ('stan', models.CharField(max_length=500)),
                ('jednostki_numer', models.CharField(max_length=50, null=True)),
                ('obreb_numer', models.CharField(max_length=50, null=True)),
                ('numer_dzialki', models.CharField(max_length=50, null=True)),
                ('identyfikator', models.CharField(max_length=50, null=True)),
                ('numer_arkusza_dzialki', models.CharField(blank=True, max_length=50, null=True)),
                ('nazwisko_projektanta', models.CharField(blank=True, max_length=50, null=True)),
                ('imie_projektanta', models.CharField(blank=True, max_length=50, null=True)),
                ('projektant_numer_uprawnien', models.CharField(blank=True, max_length=200, null=True)),
                ('projektant_pozostali', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]