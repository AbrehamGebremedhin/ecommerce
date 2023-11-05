from rest_framework.serializers import ModelSerializer
from orders.models import Order
from accounts.serializers import UserSerializer


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'creator',
            'quantity',
            'type',
            'detail',
        )
