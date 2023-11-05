from django.urls import path
from products.views import ProductFetch, ProductCreate, ProductDetail, ImageCreateFetch, ImageDetail

urlpatterns = [
    path('products/', ProductFetch.as_view(), name='Fetch all Products'),
    path('productcreate/', ProductCreate.as_view(), name='Add Product'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='Update Product'),
    path('images/<int:pk>/', ImageCreateFetch.as_view(), name='Add and Fetch All Products Image'),
    path('image/<int:pk>/', ImageDetail.as_view(), name='View and delete Specific Product Image')
]
