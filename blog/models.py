from lib2to3.pgen2 import token
from statistics import mode
from django.conf import Settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import geocoder
from tomlkit import key

# class Users(AbstractUser):
#     is_customer=models.BooleanField(default=False)
#     is_restaurant=models.BooleanField(default=False)
class Post(models.Model):
    LABELS = (
        ('Best Selling Foods', 'Best Selling Foods'),
        ('New Food', 'New Food'),
        ('Spicy Foods', 'Spicy Foods'),
        ('Cultural Food', 'Cultural Food'),
        ('Fasting Food', 'Fasting Food'),

    )  
    title = models.CharField(max_length=100,help_text='Enter the name of the food')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(default="foods")
    labels = models.CharField(max_length=25, default='New Food',choices=LABELS, blank=True)
    pieces = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    image = models.ImageField(default='default.jpg', upload_to='images/')
    image2 = models.ImageField(default='default.jpg', upload_to='images/')

    def __str__(self) :
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})   

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)   

# class Product(models.model):
#     name=models.CharField(max_length=200)
#     price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)         
#     def __str__(self):
#         return self.name
class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    # restaurant=models.ForeignKey(Post,on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(default=timezone.now)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.customer) 

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total  

class Address(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
    location=models.CharField(max_length=200,null=True,blank=True)
    lat=models.FloatField(blank=True,null=True)
    long = models.FloatField(blank=True,null=True)

    def save(self,*args,**kwargs):
        g=geocoder.osm(self.location)
        
        g=g.latlng
        self.lat=g[0]
        self.long=g[1]
        return super(Address,self).save(*args,**kwargs)
    def __str__(self):
        return '%s' % (self.location)
        
class rregister(models.Model):
    restaurant_name=models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    restaurant_logo=models.ImageField(default='logo.jpg', upload_to='profile_pics')
    phone = models.IntegerField(null=True)
    Bio =models.TextField(max_length=1000000)
    email = models.EmailField(null=True)
    location = models.ForeignKey(Address,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  

    def __str__(self):
        return '%s' % (self.restaurant_name)

     
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class register(models.Model):
    customer_name=models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    location = models.TextField(null=True,)

    def __str__(self):
        return '%s' % (self.customer_name)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})        

   

class OrderItem(models.Model):
    ORDER_STATUS = (
        ('Active', 'Active'),
        ('Delivered', 'Delivered')
    )
    Customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    ordered_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Active')
    
    def  get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={'pk' : self.pk})


    def __str__(self):
        return '%s' % (self.status)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
rate_choices = ((1, 'bad'), (2, 'not tasty'),(3,'ok'),(4,'good'),(5,'delicious'))
class Comment(models.Model):

    post = models.ForeignKey(Post,related_name='comments',on_delete = models.CASCADE)
    name = models.TextField()
    rslug=models.SlugField()
    review = models.TextField()
    rating=models.IntegerField(choices=rate_choices,blank=True,null=True)
    posted_on = models.DateField(default=timezone.now)
    likes = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return '%s - %s' % (self.post.title,self.name) 


      

