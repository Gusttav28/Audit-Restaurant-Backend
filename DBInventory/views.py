from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.shortcuts import render, get_object_or_404
from .serializer import *
from .models import *

# Create your views here.

class InventoryTable_View(APIView):
    def get(self, request):
        tables = InventoryTypes_Tables.objects.all()
        serializer =  InventoryTypes_Tables_Serializer(tables, many = (True))
        return Response(serializer.data)
    
    def post(self, request):
        serializer = InventoryTypes_Tables_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryItemView(APIView):
    def get(self, request, table_id):
        table = get_object_or_404(InventoryTypes_Tables, id=table_id)
        items = InventoryItems.objects.filter(table_ref = table)
        
        serializer = IventoryItems_Serializer(
            items, 
            many=True,
            context = {
                "table_instance": table.table,
                "table_model": table
            }
        )
        
        return Response(serialzer.data, status=status.HTTP_200_OK)

    def post(self, request, table_id):
        table = get_object_or_404(InventoryTypes_Tables, id=table_id)
        
        serializer = IventoryItems_Serializer(
            items, 
            many=True,
            context = {
                "table_instance": table.table,
                "table_model": table
            }
        )
        
        if serializer.is_valid():
            item = serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)