from django.db import models
from accounts.models import User


# Create your models here.
class Order(models.Model):
    type = models.CharField(max_length=30)
    detail = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')

    def __str__(self):
        return self.type
