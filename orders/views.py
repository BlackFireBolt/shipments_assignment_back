from rest_framework import generics, mixins, viewsets

from .models import Order, Item
from .serializers import OrderSerializer, ItemSerializer


class OrderApiView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class ItemApiView(generics.CreateAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class ItemDeliteApiView(generics.DestroyAPIView):
    queryset = Item.objects.all()