from django.urls import path
from cart.views import CartCreateFetch, CartDetail, ItemAdd, ItemDetail, CheckCart

urlpatterns = [
    path('carts/', CartCreateFetch.as_view(), name='Fetch all Cart and create a new cart'),
    path('cart/<int:pk>/', CartDetail.as_view(), name='Update Cart'),
    path('additem/', ItemAdd.as_view(), name='Add an item to a cart'),
    path('item/<int:pk>/', ItemDetail.as_view(), name='Update item information'),
    path('check/', CheckCart.as_view(), name='Check Cart')
]
