from django.urls import path
from accounts.views import UserFetch, UserCreate, UserDetail, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='Login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='Refresh'),
    path('users/', UserFetch.as_view(), name='Fetch all users'),
    path('usercreate/', UserCreate.as_view(), name='Create User'),
    path('user/<int:pk>/', UserDetail.as_view(), name ='User Update')
]
