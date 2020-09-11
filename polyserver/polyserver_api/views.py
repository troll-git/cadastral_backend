from django.shortcuts import render
from rest_framework import viewsets
from .models import Dzialki
from .serializers import DzialkiSerializer
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
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['name']
    #print('user')
