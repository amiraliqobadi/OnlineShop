# Register your models here.
from django.contrib import admin
from .models import Payment, Shipment

admin.site.register((Payment, Shipment))
