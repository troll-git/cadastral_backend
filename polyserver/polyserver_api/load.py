import os
from django.contrib.gis.utils import LayerMapping
from .models import Dzialki

dzialki_mapping = {
    'gid' : 'gid',
    'objectid' :'objectid',
    'identyfikator' :'identyfika',
    'powierzchnia':'powierzchn',
    'teryt':'teryt',
    'numer':'numer',
    'wojewodztwo':'wojewodztw',
    'powiat':'powiat',
    'gmina':'gmina',
    'data_od':'data_od',
    'length':'shape_leng',
    'area':'shape_area',
    'mpoly':'MULTIPOLYGON',
}

dane_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../data', 'malopolska.shp'),
)

def run(verbose=True):
    print(dane_shp)
    lm = LayerMapping(Dzialki, dane_shp, dzialki_mapping, transform=True)
    lm.save(strict=True, verbose=verbose)


