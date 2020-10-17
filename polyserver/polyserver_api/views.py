from django.shortcuts import render
from rest_framework import viewsets
from .models import Dzialki
from .models import Pozwolenia
from .models import PozwoleniaGeom
from .models import WnioskiGeom
from .serializers import DzialkiSerializer
from .serializers import PozwoleniaSerializer
from .serializers import PozwoleniaGeomSerializer
from .serializers import PozwoleniaGeomSerializerPoints
from .serializers import WnioskiGeomSerializerPoints
from .serializers import WnioskiGeomSerializer
from django.contrib.gis.geos import Polygon
from django.core.serializers import serialize
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
# Create your views here.


class DzialkiViewSet(viewsets.ModelViewSet):
    queryset =Dzialki.objects.all()
    serializer_class = DzialkiSerializer

    def createPoly(self,xmin,ymin,xmax,ymax):
        poly = Polygon(((ymin,xmin ), (ymin, xmax), (ymax, xmax), (ymax, xmin), (ymin, xmin)))
        return poly

    def get_queryset(self):
        bbox = self.request.query_params.get('bbox',None)
        queryset = Dzialki.objects.all()
        bounds=bbox.split(',')
        polygon = self.createPoly(float(bounds[0]),float(bounds[1]),float(bounds[2]),float(bounds[3]))
        print (bbox.split(','))
        #polygon = Polygon(((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0)))
        if bbox is not None:
            queryset = Dzialki.objects.filter(mpoly__bboverlaps=polygon)
            print(bbox)
        return queryset

class PozwoleniaViewSet(viewsets.ModelViewSet):
    queryset = Pozwolenia.objects.all()
    serializer_class = PozwoleniaSerializer

    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['name']


class PozwoleniaGeomViewSet(viewsets.ModelViewSet):
    queryset = PozwoleniaGeom.objects.all()
    serializer_class = PozwoleniaGeomSerializerPoints

    def createPoly(self,xmin,ymin,xmax,ymax):
        poly = Polygon(((ymin,xmin ), (ymin, xmax), (ymax, xmax), (ymax, xmin), (ymin, xmin)))
        return poly

    def get_queryset(self):
        bbox = self.request.query_params.get('bbox',None)
        queryset = PozwoleniaGeom.objects.all()
        bounds=bbox.split(',')
        polygon = self.createPoly(float(bounds[0]),float(bounds[1]),float(bounds[2]),float(bounds[3]))
        print (bbox.split(','))
        #polygon = Polygon(((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0)))
        if bbox is not None:
            queryset = PozwoleniaGeom.objects.filter(point__bboverlaps=polygon)
            print(bbox)
        return queryset

class PozwolenieSingleViewSet(viewsets.ModelViewSet):
    queryset = PozwoleniaGeom.objects.all()
    serializer_class = PozwoleniaGeomSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id',None)
        queryset = PozwoleniaGeom.objects.all()

        if id is not None:
            queryset = PozwoleniaGeom.objects.filter(id=id)
            print(id)
        return queryset

class WnioskiGeomViewSet(viewsets.ModelViewSet):
    queryset = WnioskiGeom.objects.all()
    serializer_class = WnioskiGeomSerializerPoints

    def createPoly(self,xmin,ymin,xmax,ymax):
        poly = Polygon(((ymin,xmin ), (ymin, xmax), (ymax, xmax), (ymax, xmin), (ymin, xmin)))
        return poly

    def get_queryset(self):
        bbox = self.request.query_params.get('bbox',None)
        queryset = WnioskiGeom.objects.all()
        bounds=bbox.split(',')
        polygon = self.createPoly(float(bounds[0]),float(bounds[1]),float(bounds[2]),float(bounds[3]))
        print (bbox.split(','))
        #polygon = Polygon(((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0)))
        if bbox is not None:
            queryset = WnioskiGeom.objects.filter(point__bboverlaps=polygon)
            print(bbox)
        return queryset

class WniosekSingleViewSet(viewsets.ModelViewSet):
    queryset = WnioskiGeom.objects.all()
    serializer_class = WnioskiGeomSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id',None)
        queryset = WnioskiGeom.objects.all()

        if id is not None:
            queryset = WnioskiGeom.objects.filter(id=id)
            print(id)
        return queryset