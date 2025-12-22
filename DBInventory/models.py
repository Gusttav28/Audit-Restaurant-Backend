from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models import JSONField

# Here we have the models of the project, that in this case are dynamic models.
# Basically with a dynamic model a user can creates different tables on the db without affecting the main structure of this one.

# in this class we're creating the user is gonna create they tables.
class InventoryTypesTables(models.Model):
    name = models.CharField(max_length=100)
    table = JSONField()
    

# in this class the user is gonna create base on the colums that this one added to his new tables the items for each of this columns.
class InventoryItems(models.Model):
    name = models.ForeignKey(InventoryTypesTables, on_delete=models.CASCADE)
    data = JSONField()