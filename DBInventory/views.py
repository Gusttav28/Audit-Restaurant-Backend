from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, exceptions
from django.shortcuts import render, get_object_or_404
from .serializer import *
from .models import InventoryTypesTables, InventoryItems, TableTest, CustomTable
from .services import create_custom_table

#just for branch testingdb

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

# Create your views here.

class InventoryTableView(APIView):
    def get(self, request):
        tables = InventoryTypesTables.objects.all()
        serializer =  InventoryTypesTablesSerializer(tables, many = (True))
        return Response(serializer.data)
    
    def post(self, request):
        serializer = InventoryTypesTablesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryItemView(APIView):
    def get(self, request, pk):
        table = get_object_or_404(InventoryTypesTables, id=pk)
        items = InventoryItems.objects.filter(name_id = table)
        
        serializer = IventoryItemsSerializer(
            items, 
            many=True,
            context = {
                "table_instance": table.table,
                "table_model": table
            }
        )
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        table = get_object_or_404(InventoryTypesTables, id=pk)
        
        serializer = IventoryItemsSerializer(
            data = request.data,
            context = {
                "table_instance": table.table,
                "table_model": table
            }
        )
        
        if serializer.is_valid():
            items = serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

# views for testingdb
# @csrf_exempt
# def TableTestView(request):
#     if request.method == "GET":
#         table = TableTest.objects.all()
#         serializer = TestTableModelSerializer(table, many=True)
#         return JsonResponse(serializer.data, safe=False)
    
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = TestTableModelSerializer(data = data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status = 201)
#         return JsonResponse(serializer.errors, status=400)


# @csrf_exempt
# def TableTest_detail(request, pk):
#     try:
#         table = TableTest.objects.get(pk=pk)
#     except TableTest.DoesNotExist:
#         return HttpResponse(status = 404)

#     if request.method == "GET":
#         serializer = TestTableModelSerializer(table)
#         return JsonResponse(serializer.data)
    
#     elif request.method == "PUT":
#         data = JSONParser().parse(request)
#         serializer = TestTableModelSerializer(table, data = data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
    
#     elif request.method == "DELETE":
#         table.delete()
#         return HttpResponse(status = 204)
    


class TableTestViewSerializer(viewsets.ModelViewSet):
    queryset = TableTest.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TestTableModelSerializer

class InventoryTableTestView(viewsets.ModelViewSet):
    queryset = InventoryTypesTables.objects.all()
    serializer_class = InventoryTableTest

class InventoryItemTestView(viewsets.ModelViewSet): 
    serializer_class = InventoryItemTest

    def get_queryset(self):
        schema_id = self.kwargs.get('schema_pk')
        return InventoryItems.objects.filter(schema_id = schema_id)
    
    def perform_create(self, serializer):
        schema_id = self.kwargs.get('schema_pk')
        try:
            schema = InventoryTypesTables.objects.get(pk = schema_id)
            serializer.save(schema = schema)
        except InventoryTypesTables.DoesNotExist:
            raise exceptions.NotFound("The specified Inventory doesn not exist")


@api_view(["POST"])
def create_table(request):
    serializer = CustomTableSerializer(data = request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        create_custom_table(
            data["customer_id"],
            data["table_name"],
            data["schema"]
        )
        return Response({"message":"Tablee was created successfully"})

    return Response(serializer.errors, status=400)

@api_view(["GET"])
def get_table(request, table_name):
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM {table_name}')
        columns = [col[0] for  col in cursor.description]
        rows = cursor.fetchall()

    data = [dict(zip(columns, row)) for row in rows]
    return Response(data)


class TablesView(viewsets.ModelViewSet):
    serializer_class = CustomTableSerializer

    def get_queryset(self):
        customer_id = self.kwargs.get('customer_id')
        return CustomTable.objects.filter(customer_id=customer_id)