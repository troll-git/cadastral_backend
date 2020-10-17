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

router = routers.DefaultRouter()
router.register('dzialki',DzialkiViewSet)
router.register('pozwolenia',PozwoleniaViewSet)
router.register('pozwolenia_geom',PozwoleniaGeomViewSet)
router.register('pozwolenie',PozwolenieSingleViewSet)
router.register('wnioski_geom',WnioskiGeomViewSet)
router.register('wniosek',WniosekSingleViewSet)



#router.register('users',UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]