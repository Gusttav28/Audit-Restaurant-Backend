from . import views
from .views import InventoryTableTestView, InventoryItemTestView, create_table, get_table, TablesView
from django.urls import path, include
from rest_framework_nested import routers as nested_routers
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'InventoryTable', InventoryTableTestView, basename="InventoryTable")

router = routers.DefaultRouter()
router.register(r'tables', TablesView, basename="tables")


# schema_router = nested_routers.NestedDefaultRouter(router, r'InventoryTable', lookup = 'InventoryTable')
# schema_router.register(r'InventoryItem', InventoryItemTestView, basename='InventoryItem')


urlpatterns = [
    # path('', include(router.urls),
    # path('', include(schema_router.urls))
    path('customTables/create/', create_table, name = "create_custom_table"),
    path('tables/<str:table_name>/rows/', get_table)
]
