from django.urls import path
from .views import ItemApiView, ItemDeliteApiView, OrderApiView, OrderDetailApiView


app_name = 'orders'

urlpatterns = [
    path('', OrderApiView.as_view(), name="order_list"),
    path('<int:pk>/', OrderDetailApiView.as_view(), name='order_detail'),
    path('item/', ItemApiView.as_view(), name='item_list'),
    path('item/<int:pk>/', ItemDeliteApiView.as_view(), name='item_detail')
]