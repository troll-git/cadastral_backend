from rest_framework import serializers
from django.core.serializers import serialize
from .models import Dzialki
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class DzialkiSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Dzialki
        fields = ['gid','objectid','identyfikator','powierzchnia','teryt','numer','wojewodztwo','powiat','gmina','data_od','length','area']
        geo_field = 'mpoly'
        #def create(self,validated_data):
        #    return Dzialki(**validated_data)