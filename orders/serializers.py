from dataclasses import field
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from rest_framework import serializers

from .models import Order, Item


class ItemSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'order', 'name', 'description', 'quantity', 'created_date',
                  'updated_date')
        extra_kwargs = {'id': {'read_only': False, 'required': False}}

class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'shipment_number', 'loading_point', 'unloading_point', 'created_date',
                  'updated_date', 'load_date', 'unload_date', 'tracking_number', 'status', 'items')


    def create(self, validated_data):
        items = validated_data.pop('items')
        order = Order(**validated_data)
        order.save()
        for item in items:
            Item.objects.create(order=order, **item)
        return order
    
    def update(self, instance, validated_data):
        instance.shipment_number = validated_data.get('shipment_number', instance.shipment_number)
        instance.loading_point = validated_data.get('loading_point', instance.loading_point)
        instance.unloading_point = validated_data.get('unloading_point', instance.unloading_point)
        instance.load_date = validated_data.get('load_date', instance.load_date)
        instance.unload_date = validated_data.get('unload_date', instance.unload_date)
        instance.tracking_number = validated_data.get('tracking_number', instance.tracking_number)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        items = validated_data.get('items')
        for item in items:
            item_id = item.get('id', None)
            if item_id:
                inv_item = get_object_or_404(Item, pk=item_id)
                inv_item.name = item.get('name', inv_item.name)
                inv_item.description = item.get('description', inv_item.description)
                inv_item.quantity = item.get('quantity', inv_item.quantity)
                inv_item.save()
            else:
                Item.objects.create(order=instance, **item)

        return instance
