import os
from django.contrib.gis.utils import LayerMapping
from .models import Dzialki
from .models import Pozwolenia

dzialki_mapping = {
    #'gid' : 'gid',
    'objectid' :'OBJECTID',
    'identyfikator' :'IDENTYFIKA',
    'powierzchnia':'POWIERZCHN',
    'teryt':'TERYT',
    'numer':'NUMER',
    'wojewodztwo':'WOJEWODZTW',
    'powiat':'POWIAT',
    'gmina':'GMINA',
    'data_od':'DATA_OD',
    'length':'Shape_Leng',
    'area':'Shape_Area',
    'mpoly':'MULTIPOLYGON',
}

powzolenia_mapping = {
    'numer_urzad' :'numer_urzad',
    'nazwa_organu':'nazwa_organu',
    'adres_organu':'adres_organu',
    'data_wplywu_wniosku': 'data_wplywu_wniosku',
    'numer_decyzji_urzedu':'numer_decyzji_urzedu',
    'data_wydania_decyzji':'data_wydania_decyzji' ,
    'nazwisko_inwestora': 'nazwisko_inwestora',
    'imie_inwestora':'imie_inwestora',
    'nazwa_inwestor':'nazwa_inwestor',
    'wojewodztwo':'wojewodztwo',
    'miasto':'miasto',
    'terc':'terc',
    'cecha':'cecha',
    'ulica':'ulica',
    'ulica_dalej': 'ulica_dalej' ,
    'nr_domu' :'nr_domu',
    'rodzaj_inwestycji': 'rodzaj_inwestycji',
    'kategoria': 'kategoria',
    'nazwa_zamierzenia_bud' :'nazwa_zamierzenia_bud',
    'nazwa_zam_budowlanego':'nazwa_zam_budowlanego',
    'projektant_nazwisko': 'projektant_nazwisko' ,
    'projektant_numer_uprawnien':'projektant_numer_uprawnien',
    'jednostka_numer_ew':'jednostka_numer_ew',
    'obreb_numer' :'obreb_numer' ,
    'numer_dzialki':'numer_dzialki',
    'kod_dzialki' :'kod_dzialki',
    'numer_arkusza_dzialki':'numer_arkusza_dzialki',
    'jednostka_stara_numeracja_z_wniosku': 'jednostka_stara_numeracja_z_wniosku',
    'stara_numeracja_obreb_z_wniosku':'stara_numeracja_obreb_z_wniosku',
    'stara_numeracja_dzialka_z_wniosku':'stara_numeracja_dzialka_z_wniosku'
}

dane_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../data/slsk', 'slsk.shp'),
)

dane_csv = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../data', 'testbud.csv'),
)

def run(verbose=True):
    print(dane_shp)
    lm = LayerMapping(Dzialki, dane_shp, dzialki_mapping, transform=True)
    lm.save(strict=True, verbose=verbose)


