from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.models import User
from accounts.serializers import UserSerializer, CustomTokenObtainPairSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer


# Create your views here.
class UserCreate(APIView):
    def post(self, request):
        """Create a new user"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFetch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List all the users in the system"""
        permission_classes = [IsAuthenticated]
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetail(APIView):
    """To update a specific user"""
    permission_classes = [IsAuthenticated]

    def get_user(self, pk):
        """Fetches a specific user for get, update and delete functions"""
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Http404

    def get(self, request, pk):
        user = self.get_user(pk)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        user = self.get_user(pk)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_user(pk)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenObtainPairSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

