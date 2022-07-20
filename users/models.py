from django.db import models
from django.contrib.auth.models import User,AbstractUser
from PIL import Image



# class Users(AbstractUser):
#     is_restaurant = models.BooleanField(default=False)
#     is_customer = models.BooleanField(default=False)

# class Restaurant(models.model):
#     pass

# class Customer(models.Model):
#     pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
