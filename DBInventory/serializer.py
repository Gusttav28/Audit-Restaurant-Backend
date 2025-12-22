from rest_framework import serializers
from .models import InventoryTypesTables, InventoryItems

#This is the serializer that the model needs to transform the data of the settings from sql data to json api
class InventoryTypesTablesSerializer(serializers.ModelSerializer):
    # validation function of the tables that are creating
    def validate_tables(self, value):
        allowed_types = {"string", "number", "created_at"}
        fields = value.get("fieds", {})
        
        if not fields:
            raise serializers.ValidationError("The table must have at least one field.")
        
        for field_name, field_type in fields.items():
            if field_type not in allowed_types:
                raise serializers.ValidationError(
                    f"Invalid type '{field_type}' for field '{field_name}'"
                )
        return value

    class Meta:  
        model = InventoryTypesTables
        fields = "__all__"
        
        
class IventoryItemsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        
        # # attrs = attributes
        # def validate(self, attrs):
        #     if not attrs:
        #         raise serializers.ValidationError(
        #             "No valid fields provided for this table."
        #         )
        #     return attrs
        
        table_instance = self.context.get('table_instance')
        
        if table_instance:
            for field_name, field_type in table_instance['fields'].items():
                if field_type == 'string':
                    self.fields[field_name] = serializers.CharField()
                elif field_type == 'number':
                    self.fields[field_name] = serializers.IntegerField()
                elif field_type == 'created_at':
                    self.fields[field_name] = serializers.DateTimeField()
        
    def create(self, validated_data):
            table = self.context['table_model']
            return InventoryItems.objects.create(
                table_ref = table,
                data = validated_data
            )
            
    def to_representation(self, table_instance):
            return table_instance.data 
        
    class Meta:  
        model = InventoryItems
        fields = "__all__"