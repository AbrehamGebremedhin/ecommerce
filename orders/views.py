from orders.models import Order
from orders.serializers import OrderSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# Create your views here.
class OrderCreate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @staticmethod
    def post(request):
        """Create a new custom order"""
        serializer = OrderSerializer(data={
            'creator': request.user.pk,
            'quantity': request.data['quantity'],
            'type': request.data['type'],
            'detail': request.data['detail'],
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderFetch(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request):
        """List all the orders in the system"""
        orders = Order.objects.all()

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetail(APIView):
    """To update a specific order"""
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_order(pk):
        """Fetches a specific order for the usage of get, patch and delete functions"""
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Http404

    def get(self, request, pk):
        order = self.get_order(pk)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        order = self.get_order(pk)
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_order(pk)
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

