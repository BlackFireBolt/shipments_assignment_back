from pyexpat import model
import uuid
from django.db import models


class Order(models.Model):
    shipment_number = models.UUIDField(default=uuid.uuid4, editable=False)
    loading_point = models.CharField(max_length=64)
    unloading_point = models.CharField(max_length=64)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    load_date = models.DateField()
    unload_date = models.DateField()
    tracking_number = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=64)

    def __str__(self):
        return self.shipment_number

    class Meta:
        ordering = ['-created_date', '-updated_date']


class Item(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    quantity = models.IntegerField()
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-created_date', '-updated_date']
