from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Dzialki
from .models import Pozwolenia
from .models import PozwoleniaGeom
from .models import Wnioski
from .models import WnioskiGeom
from .models import Update
from .models import IpData
from .models import Contact
from .serializers import DzialkiSerializer
from .serializers import PozwoleniaSerializer
from .serializers import PozwoleniaGeomSerializer
from .serializers import PozwoleniaGeomSerializerPoints
from .serializers import WnioskiGeomSerializerPoints
from .serializers import WnioskiGeomSerializer
from .serializers import UpdateSerializer
from .serializers import IpDataSerializer
from .serializers import ContactSerializer
from django.contrib.gis.geos import Polygon
from datetime import datetime
from django.core.serializers import serialize
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db.models import Avg, Max, Min, Sum
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

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

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def get(self,request,format=None):
        bbox = self.request.query_params.get('bbox',None)
        start_date = self.request.query_params.get('start_date',None)
        end_date = self.request.query_params.get('end_date', None)
        category = self.request.query_params.get('category',None)
        investor = self.request.query_params.get('investor',None)
        if start_date == "undefined" or start_date=="" or start_date==None:
            start_date="2000-01-01"
        if end_date == "undefined" or end_date==""or end_date==None:
            end_date=datetime.now().date()
        queryset = PozwoleniaGeom.objects.all()
        bounds=bbox.split(',')
        polygon = self.createPoly(float(bounds[0]),float(bounds[1]),float(bounds[2]),float(bounds[3]))
        print (bbox.split(','))
        if bbox is not None :
            print("notnone")
            queryset = PozwoleniaGeom.objects.filter(point__bboverlaps=polygon).filter(data_wydania_decyzji__gte=start_date).filter(data_wydania_decyzji__lt=end_date)
        if category != None and category !="undefined" and category !="":
            queryset=queryset.filter(kategoria=category)
        if investor != None and investor !="undefined" and investor !="":
            queryset=queryset.filter(Q(nazwisko_inwestora__icontains=investor)|Q(imie_inwestora__icontains=investor)|Q(nazwa_inwestor__icontains=investor))
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
        start_date = self.request.query_params.get('start_date',None)
        end_date = self.request.query_params.get('end_date', None)
        category = self.request.query_params.get('category',None)
        if start_date == "undefined" or start_date=="" or start_date==None:
            start_date="2000-01-01"
        if end_date == "undefined" or end_date==""or end_date==None:
            end_date=datetime.now().date()
        queryset = WnioskiGeom.objects.all()
        bounds=bbox.split(',')
        polygon = self.createPoly(float(bounds[0]),float(bounds[1]),float(bounds[2]),float(bounds[3]))
        print (bbox.split(','))
        if bbox is not None:
            queryset = WnioskiGeom.objects.filter(point__bboverlaps=polygon).filter(data_wplywu_wniosku_do_urzedu__gte=start_date).filter(data_wplywu_wniosku_do_urzedu__lt=end_date)
        if category != None and category !="undefined" and category !="":
            queryset=queryset.filter(kategoria=category)
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

class StatsViewSet(viewsets.ViewSet):
    def list(self,request,format=None):
        number_of_wnioski=WnioskiGeom.objects.all().count()
        return Response({"wnioski":Wnioski.objects.all().count(),
                        "pozwolenia":Pozwolenia.objects.all().count(),
                        "wnioski_geom":WnioskiGeom.objects.all().count(),
                        "pozwolenia_geom":PozwoleniaGeom.objects.all().count(),
                        "dzialki":Dzialki.objects.all().count()})

class UpdateViewSet(viewsets.ModelViewSet):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    
    def get_queryset(self):
        max_id=Update.objects.latest('id').id
        print(max_id)
        queryset = Update.objects.filter(id=max_id)
        return queryset

class IpDataViewSet(viewsets.ModelViewSet):
    queryset = IpData.objects.all()
    serializer_class = IpDataSerializer

    #@action(detail=False,methods=['POST'])
    #def sendIp(self,request,pk,format=None):
    #    print(request.data)
    #    resp={'mess':"it is"}
    #    return Response(resp,status=status.HTTP_200_OK)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self):
        queryset = Contact.objects.filter(id=1)
        return queryset
