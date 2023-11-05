from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class ProductImage(models.Model):
    def rename_image(self, filename):
        return f"static/product_images/{self.product}.jpg"
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=rename_image)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product
