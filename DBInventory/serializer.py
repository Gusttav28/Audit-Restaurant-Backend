from rest_framework import serializers
from .models import InventoryTypesTables, InventoryItems, TableTest, CustomTable

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


# working with serialzers 
class TestTableSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    item_name = serializers.CharField(required = True, allow_blank = True, max_length=100)
    quantity = serializers.IntegerField(required = False, default = 1)

    def create(self, validad_data):
        return TableTest.create(**validad_data)
    
    def update(self, instance, validated_data):
        instance.item_name = validated_data.get("item_name", instance.title )
        instance.quantity = validated_data.get("quantity", instance.quantity )
        instance.save()
        return instance
    

# working with ModelSerializer

class TestTableModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableTest
        fields = "__all__"


class InventoryTableTest(serializers.ModelSerializer):
    class Meta:
        model = InventoryTypesTables
        fields = "__all__"

class InventoryItemTest(serializers.ModelSerializer):
    # table = serializers.SlugRelatedField(read_only = True, slug_field = id)
    class Meta:
        model = InventoryItems
        fields = "__all__"

    def validate(self, attrs):
        schema = attrs.get('schema')
        data = attrs.get('data')

        allowed_fields = schema.table.get('fields', [])

        for key in data.keys():
            if key not in allowed_fields:
                raise serializers.ValidationError(f"Field '{key}' is not defined in the {schema.name} schema.")
            
        return attrs


class CustomTableSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    table_name = serializers.CharField(max_length = 100)
    schema = serializers.DictField()


class CustomTableSerializer2(serializers.ModelSerializer):
    class Meta:
        model = CustomTable
        fields = "__all__"