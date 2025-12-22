from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.shortcuts import render, get_object_or_404
from .serializer import InventoryTypesTablesSerializer, IventoryItemsSerializer
from .models import InventoryTypesTables, InventoryItems

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
    def get(self, request, table_id):
        table = get_object_or_404(InventoryTypesTables, id=table_id)
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

    def post(self, request, table_id):
        table = get_object_or_404(InventoryTypesTables, id=table_id)
        
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