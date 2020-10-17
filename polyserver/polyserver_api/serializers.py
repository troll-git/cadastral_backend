from rest_framework import serializers
from django.core.serializers import serialize
from .models import Dzialki
from .models import Pozwolenia
from .models import PozwoleniaGeom
from .models import WnioskiGeom
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class DzialkiSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Dzialki
        fields = ['objectid','identyfikator','powierzchnia','teryt','numer','wojewodztwo','powiat','gmina','data_od','length','area']
        geo_field = 'mpoly'
        #def create(self,validated_data):
        #    return Dzialki(**validated_data)

class PozwoleniaSerializer(serializers.ModelSerializer):
    class Meta:
        model= Pozwolenia
        fields = ['numer_urzad','nazwa_organu','adres_organu','data_wplywu_wniosku','numer_decyzji_urzedu','data_wydania_decyzji','nazwisko_inwestora',
    'imie_inwestora','nazwa_inwestor','wojewodztwo','miasto','terc','cecha','ulica','ulica_dalej','nr_domu','rodzaj_inwestycji','kategoria',
    'nazwa_zamierzenia_bud','nazwa_zam_budowlanego','projektant_nazwisko','projektant_numer_uprawnien','jednostka_numer_ew','obreb_numer',
    'numer_dzialki','identyfikator','numer_arkusza_dzialki','jednostka_stara_numeracja_z_wniosku','stara_numeracja_obreb_z_wniosku','stara_numeracja_dzialka_z_wniosku','created_at']

class PozwoleniaGeomSerializer(serializers.ModelSerializer):
    class Meta:
        model= PozwoleniaGeom
        fields = ['numer_urzad','nazwa_organu','adres_organu','data_wplywu_wniosku','numer_decyzji_urzedu','data_wydania_decyzji','nazwisko_inwestora',
    'imie_inwestora','nazwa_inwestor','wojewodztwo','miasto','terc','cecha','ulica','ulica_dalej','nr_domu','rodzaj_inwestycji','kategoria',
    'nazwa_zamierzenia_bud','nazwa_zam_budowlanego','kubatura','projektant_nazwisko','projektant_numer_uprawnien','jednostka_numer_ew','obreb_numer',
    'numer_dzialki','identyfikator','numer_arkusza_dzialki','jednostka_stara_numeracja_z_wniosku','stara_numeracja_obreb_z_wniosku','stara_numeracja_dzialka_z_wniosku']

class PozwoleniaGeomSerializerPoints(GeoFeatureModelSerializer):
    class Meta:
        model= PozwoleniaGeom
        fields = ['id']
        geo_field = 'point'

class WnioskiGeomSerializer(serializers.ModelSerializer):
    class Meta:
        model = WnioskiGeom
        fields= ['numer_ewidencyjny_system', 'numer_ewidencyjny_urzad', 'data_wplywu_wniosku_do_urzedu','nazwa_organu', 'wojewodztwo_objekt',
        'obiekt_kod_pocztowy', 'miasto', 'terc', 'cecha', 'ulica', 'ulica_dalej', 'nr_domu', 'kategoria', 'nazwa_zam_budowlanego', 'rodzaj_zam_budowlanego',
        'kubatura', 'stan', 'jednostki_numer', 'obreb_numer', 'numer_dzialki', 'identyfikator', 'numer_arkusza_dzialki', 'nazwisko_projektanta',
        'imie_projektanta', 'projektant_numer_uprawnien', 'projektant_pozostali']

class WnioskiGeomSerializerPoints(GeoFeatureModelSerializer):
    class Meta:
        model= WnioskiGeom
        fields = ['id']
        geo_field = 'point'