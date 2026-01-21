from django.db import connection


ALLOWED_TYPES = {
    "text": "TEXT",
    "integer": "INTEGER",
    "decimal": "DECIMAL(10,2)",
}

def validate_schema(schema):
    for field, field_type in schema.items():
        if field_type not in ALLOWED_TYPES:
            raise ValueError("Invalid field type")


def create_custom_table(customer_id, table_name, schema):
    validate_schema(schema)

    columns = []
    for field, field_type in schema.items():
        sql_type = ALLOWED_TYPES[field_type]
        columns.append(f'{field} {sql_type}')
    
    safe_table_name = f'customer_{customer_id}_{table_name}'
    sql = f"""
        CREATE TABLE IF NOT EXISTS {safe_table_name} (
            id SERIAL PRIMARY KEY,
            {', '.join(columns)}
        )
    """

    with connection.cursor() as cursor:
        cursor.execute(sql)
