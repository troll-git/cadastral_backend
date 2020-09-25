from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from django.conf.urls import include
from .views import DzialkiViewSet


router = routers.DefaultRouter()
router.register('dzialki',DzialkiViewSet)
router.register('dzialki', DzialkiViewSet , basename='Dzialki')
#router.register('users',UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]