from products.models import Product, ProductImage
from products.serializers import ProductSerializer, ImageSerializer
from products.pagination import CustomPagination
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# Create your views here.
class ProductCreate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        """Create a new user"""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductFetch(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        """List all the products in the system"""
        filter_params = {
            'color': self.request.query_params.get('color'),
            'type': self.request.query_params.get('type'),
            'size': self.request.query_params.get('size'),
        }

        min_value = self.request.query_params.get('min')
        max_value = self.request.query_params.get('max')

        for field, value in filter_params.items():
            if value is '':
                print(f"{field}: {value}")

        products = Product.objects.all()

        if any(value is not None for value in filter_params.values()):
            for field, value in filter_params.items():
                if value is not None:
                    products = products.filter(**{f"{field}__iexact": value})

        if min_value is not None and max_value is not None:
            products = products.filter(price__range=(float(min_value), float(max_value)))

        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request)

        # Serialize paginated products
        serializer = ProductSerializer(paginated_products, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)


class ProductDetail(APIView):
    """To update a specific user"""
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_product(pk):
        """Fetches a specific product for the usage of get, patch and delete functions"""
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Http404

    def get(self, request, pk):
        product = self.get_product(pk)
        # if not product:
        #     return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        product = self.get_product(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_product(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageCreateFetch(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        images = ProductImage.objects.filter(product=pk)
        if not images:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        """Add a new image"""
        data = {
            'image': request.data['image'],
            'product': pk
        }
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(APIView):
    """To update a specific image"""
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_image(pk):
        """Fetches a specific product image for the usage of get, patch and delete functions"""
        try:
            return ProductImage.objects.get(pk=pk)
        except ProductImage.DoesNotExist:
            return Http404

    def get(self, request, pk):
        image = self.get_image(pk)
        if not image:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        image = self.get_image(pk)
        if not image:
            return Response(status=status.HTTP_404_NOT_FOUND)

        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
