from . import views
from .views import *
from django.urls import path

urlpatterns = [
    path('inventory_items/<int:table_id>/items/', InventoryItemView.as_view()),
    path('inventory_table/', InventoryTable_View.as_view()),
]
