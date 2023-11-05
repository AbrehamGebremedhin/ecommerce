from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from products.models import Product, ProductImage


class ImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    pictures = serializers.ListField(child=serializers.ImageField(), write_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'size', 'color', 'price', 'type', 'quantity', 'pictures', 'images')

    def create(self, validated_data):
        images_data = validated_data.pop('pictures')
        product = Product.objects.create(**validated_data)

        for image_data in images_data:
            ProductImage.objects.create(product=product, image=image_data)

        return product
