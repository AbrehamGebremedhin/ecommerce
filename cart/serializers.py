from rest_framework.serializers import ModelSerializer
from cart.models import Cart, CartItem


class ItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = (
            'id',
            'quantity',
            'cart',
            'product'
        )


class CartSerializer(ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        subtotal = 0
        for item in instance.items.all():
            subtotal += item.quantity * item.product.price

        total = subtotal * 0.15
        data['subtotal'] = subtotal
        data['total'] = total + subtotal
        return data

    class Meta:
        model = Cart
        fields = (
            'pk',
            'user',
            'items',
            'status'
        )
