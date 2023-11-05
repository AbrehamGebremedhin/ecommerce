from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import User
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'phone_number',
            'email',
            'password',
            'username'
        ]
        extra_kwargs = {'password': {'write_only': True}}


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializer(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
