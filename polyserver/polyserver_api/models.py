from django.contrib.gis.db import models

# Create your models here.
class Dzialki(models.Model):
    gid = models.IntegerField()
    objectid = models.IntegerField()
    identyfikator = models.CharField(max_length=100)
    powierzchnia = models.FloatField()
    teryt=models.CharField(max_length=7)
    numer = models.CharField(max_length = 50)
    wojewodztwo = models.CharField(max_length = 254)
    powiat = models.CharField(max_length=254)
    gmina=models.CharField(max_length=254)
    data_od=models.DateField()
    length=models.FloatField()
    area = models.FloatField()
    mpoly = models.MultiPolygonField()

class Pozwolenia(models.Model):
    numer_urzad = models.CharField(max_length=50)
    nazwa_organu = models.CharField(max_length=50)
    adres_organu = models.CharField(max_length=50)
    data_wplywu_wniosku = models.DateField()
    numer_decyzji_urzedu = models.CharField(max_length=25)
    data_wydania_decyzji = models.DateField()
    nazwisko_inwestora  = models.CharField(max_length=20,blank=True,null=True)
    imie_inwestora = models.CharField(max_length=20,blank=True,null=True)
    nazwa_inwestor = models.CharField(max_length=50,blank=True,null=True)
    wojewodztwo = models.CharField(max_length=20)
    miasto = models.CharField(max_length=20)
    terc = models.CharField(max_length=10,blank=True,null=True)
    cecha = models.CharField(max_length=5,blank=True,null=True)
    ulica = models.CharField(max_length=20,blank=True,null=True)
    ulica_dalej = models.CharField(max_length=20,blank=True,null=True)
    nr_domu = models.CharField(max_length=10,blank=True,null=True)
    rodzaj_inwestycji = models.CharField(max_length=100)
    kategoria = models.CharField(max_length=8)
    nazwa_zamierzenia_bud = models.CharField(max_length=512)
    nazwa_zam_budowlanego = models.CharField(max_length=512)
    kubatura = models.FloatField(blank=True,null=True)
    projektant_nazwisko = models.CharField(max_length=20,blank=True,null=True)
    projektant_imie = models.CharField(max_length=20,blank=True,null=True)
    projektant_numer_uprawnien = models.CharField(max_length=25,blank=True,null=True)
    jednostka_numer_ew = models.CharField(max_length=10)
    obreb_numer = models.CharField(max_length=10)
    numer_dzialki = models.CharField(max_length=10)
    kod_dzialki = models.CharField(max_length=50)
    numer_arkusza_dzialki = models.CharField(max_length=10,blank=True,null=True)
    jednostka_stara_numeracja_z_wniosku = models.CharField(max_length=50,blank=True,null=True)
    stara_numeracja_obreb_z_wniosku = models.CharField(max_length=50,blank=True,null=True)
    stara_numeracja_dzialka_z_wniosku = models.CharField(max_length=50,blank=True,null=True)



1

