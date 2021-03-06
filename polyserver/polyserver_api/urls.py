from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from django.conf.urls import include
from .views import DzialkiViewSet
from .views import PozwoleniaViewSet
from .views import PozwoleniaGeomViewSet
from .views import PozwolenieSingleViewSet
from .views import WnioskiGeomViewSet
from .views import WniosekSingleViewSet
from .views import StatsViewSet
from .views import UpdateViewSet
from .views import IpDataViewSet
from .views import ContactViewSet

router = routers.DefaultRouter()
router.register('dzialki',DzialkiViewSet)
router.register('pozwolenia',PozwoleniaViewSet)
router.register('pozwolenia_geom',PozwoleniaGeomViewSet)
router.register('pozwolenie',PozwolenieSingleViewSet)
router.register('wnioski_geom',WnioskiGeomViewSet)
router.register('wniosek',WniosekSingleViewSet)
router.register('stats',StatsViewSet,basename='stats')
router.register('update', UpdateViewSet)
router.register('ipdata',IpDataViewSet)
router.register('contact',ContactViewSet)


#router.register('users',UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]