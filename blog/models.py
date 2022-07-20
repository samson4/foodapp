from statistics import mode
from django.conf import Settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# class Users(AbstractUser):
#     is_customer=models.BooleanField(default=False)
#     is_restaurant=models.BooleanField(default=False)

class Post(models.Model):
    title = models.CharField(max_length=100,help_text='Enter the name of the food')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(default="foods")
    pieces = models.IntegerField(default=6)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    image = models.ImageField(default='default.jpg', upload_to='images/')
    image2 = models.ImageField(default='default.jpg', upload_to='images/')

class rregister(models.Model):
    restaurant_name=models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant_logo=models.ImageField(default='logo.jpg', upload_to='profile_pics')
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    location = models.TextField(null=True)

    def __str__(self):
        return '%s' % (self.restaurant_name)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class register(models.Model):
    customer_name=models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    location = models.TextField(null=True)

    def __str__(self):
        return '%s' % (self.customer_name)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})        

class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(default=timezone.now)
    complete = models.BooleanField(default=False,null=True,blank=False)

    def __str__(self):
        return str(self.complete) 



class OrderItem(models.Model):
    ORDER_STATUS = (
        ('Active', 'Active'),
        ('Delivered', 'Delivered')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Post, on_delete=models.CASCADE)
    ordered = models.ForeignKey(Order,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Active')
    delivery_date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return '%s' % (self.status)
    



class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments',on_delete = models.CASCADE)
    name = models.TextField()
    rslug=models.SlugField()
    review = models.TextField()
    posted_on = models.DateField(default=timezone.now)

    def __str__(self):
        return '%s - %s' % (self.post.title,self.name) 




class Address(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    Item = models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
    location=models.CharField(max_length=200,null=True)

    def __str__(self):
        return '%s' % (self.location)        

