from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    def rename_image(self, filename):
        return f"static/profile_pictures/{self.phone_number}.jpg"
    phone_number = models.CharField(max_length=13, unique=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    profile_picture = models.ImageField(null=True, upload_to=rename_image)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.pk:
            # New user, encrypt the password
            self.set_password(self.password)
        super().save(*args, **kwargs)
