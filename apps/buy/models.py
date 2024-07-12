from django.db import models
from apps.core.models import TimeStampMixin
from apps.user.models import User, Order


class Payment(TimeStampMixin):
    payment_id = models.CharField(max_length=100)
    payment_status = models.BooleanField(default=False)
    payment_amount = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Shipment(TimeStampMixin):
    shipment_id = models.CharField(max_length=100)
    shipment_status = models.BooleanField(default=False)
    shipment_method = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
