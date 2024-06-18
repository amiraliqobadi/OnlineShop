# Register your models here.
from django.contrib import admin
from .models import Coupon, ImageAlbum, Product, Like, Category, Comment

admin.site.register((Coupon, ImageAlbum, Product, Like, Category, Comment))
