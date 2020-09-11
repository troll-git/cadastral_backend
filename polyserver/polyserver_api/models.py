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