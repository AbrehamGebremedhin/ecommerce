from cart.models import Cart, CartItem
from products.serializers import ProductSerializer
from products.models import Product
from cart.serializers import CartSerializer, ItemSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class CheckCart(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        carts = Cart.objects.filter(user=request.user)

        for cart in carts:
            if cart.status == 'Unpaid':
                return Response(data={'status': True, 'id': cart.pk}, status=status.HTTP_200_OK)
            else:
                return Response(data={'status': False}, status=status.HTTP_200_OK)


class CartCreateFetch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        carts = Cart.objects.filter(user=request.user)

        if not carts:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Add a new cart"""
        print(request.user.pk)
        data = {
            'user': request.user.pk,
        }
        serializer = CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetail(APIView):
    """To update a cart image"""
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_cart(pk):
        """Fetches a specific cart for the usage of get and delete functions"""
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Http404

    def get(self, request, pk):
        cart = self.get_cart(pk)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        cart = self.get_cart(pk)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart = self.get_cart(pk)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemAdd(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        """Add a new item to cart"""
        product = Product.objects.get(pk=request.data['product'])
        serializer = ItemSerializer(data=request.data)

        if int(request.data['quantity']) > product.quantity:
            return Response(data={'status': False, 'Message': 'Not enough product to accommodate the request'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetail(APIView):
    """To update a cart item"""
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_item(pk):
        """Fetches a specific cart item for the usage of get, patch and delete functions"""
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Http404

    def patch(self, request, pk):
        item = self.get_item(pk)
        if not item:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if item.quantity == 0:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = ItemSerializer(item, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_item(pk)
        if not item:
            return Response(status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
