from django.urls import path
from accounts.views import UserFetch, UserCreate, UserDetail, MyObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', MyObtainTokenPairView.as_view(), name='Login'),
    path('refresh/', TokenRefreshView.as_view(), name='Refresh'),
    path('users/', UserFetch.as_view(), name='Fetch all users'),
    path('usercreate/', UserCreate.as_view(), name='Create User'),
    path('user/<int:pk>/', UserDetail.as_view(), name ='User Update')
]
