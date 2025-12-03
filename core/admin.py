from django.contrib import admin
from .models import Painting, Category, Cart, CartItem, Order, OrderItem, Profile
# Register your models here.

admin.site.register(Painting),
admin.site.register(Category),
admin.site.register(Cart),
admin.site.register(CartItem),
admin.site.register(Order),
admin.site.register(OrderItem),
admin.site.register(Profile),
