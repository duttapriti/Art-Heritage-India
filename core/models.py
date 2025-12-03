from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.models import User
import random
import string

# Create your models here

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, default=None )
    bg_image = models.ImageField(upload_to="bg_images/", default=None, null=True )


    def __str__(self):
        return self.name

class Painting(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='paintings', default=None)
    image = models.ImageField(upload_to="products_images/", default=None, null=True )
    rating = models.DecimalField(decimal_places=1, max_digits=3, default=0.0, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=1000.00, null=True)
    
    is_new = models.BooleanField(default=False)
    is_selling = models.BooleanField(default=False)

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'profile__is_seller': True},
        related_name='paintings'
    )

    def __str__(self):
        return self.title
    

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart for {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    painting = models.ForeignKey(Painting, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f'{self.quantity} of {self.painting.title}'

    def get_total_price(self):
        return self.quantity * self.painting.price
    



class Order(models.Model):
    STATUS_CHOICES = [
        ('Placed', 'Placed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, unique=True, editable=False)  
    date_ordered = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    # New field to track the order status
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='Placed'  # Default status is "Placed" when an order is created
    )

    # Shipping address fields
    shipping_address = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zip = models.CharField(max_length=20)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username} - {self.status}"

    def get_cart_total(self):
        return sum(item.get_total() for item in self.orderitem_set.all())

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_id():
        return ''.join(random.choices(string.digits, k=15))



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    painting = models.ForeignKey(Painting, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.painting.title}"

    def get_total(self):
        return self.painting.price * self.quantity



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_seller = models.BooleanField(default=False)
    display_name = models.CharField(max_length=255, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.user.username



