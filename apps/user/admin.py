from django.contrib import admin
from .models import Otp, User, Address, Cart, Order, OrderItems, WishList

admin.site.register((Otp, User, Address, Cart, Order, OrderItems, WishList))
