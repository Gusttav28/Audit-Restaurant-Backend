from . import views
from .views import InventoryTableTestView, InventoryItemTestView
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'InventoryTable', InventoryTableTestView, basename="InventoryTable")
router.register(r'InventoryItems', InventoryItemTestView, basename="InventoryItem")


urlpatterns = [
    path('', include(router.urls))
]
