from django.urls import path
from orders.views import OrderFetch, OrderCreate, OrderDetail

urlpatterns = [
    path('createOrder/', OrderCreate.as_view(), name='Create Custom order'),
    path('fetchOrder/', OrderFetch.as_view(), name='Fetch Custom order'),
    path('orderDetail/<int:pk>/', OrderDetail.as_view(), name='Detail Custom order'),
]
