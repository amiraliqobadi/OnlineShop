from functools import partial

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampMixin, LogicalMixin
from apps.products.models import Product
from apps.user.managers import UserManager
from utils.filename import maker


class Otp(models.Model):
	expire_date = models.DateTimeField()
	otp = models.CharField(max_length=6)


class User(LogicalMixin, AbstractUser, TimeStampMixin):
	username_validator = RegexValidator(
		r"^[a-zA-Z0-9_]*$", "Only alphanumeric characters are allowed."
	)
	username = models.CharField(
		_("user name"), max_length=50, unique=True, validators=[username_validator]
	)
	email = models.EmailField(max_length=50, unique=True)
	f_name = models.CharField(max_length=50)
	l_name = models.CharField(max_length=50)
	is_active = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	addresses = models.ForeignKey(
		"Address",
		blank=True,
		related_name="addresses",
		null=True,
		on_delete=models.CASCADE,
	)
	orders = models.ForeignKey(
		"Order", blank=True, related_name="orders", null=True, on_delete=models.CASCADE
	)
	otp = models.ForeignKey("Otp", blank=True, on_delete=models.CASCADE, null=True)
	user_image = models.ImageField(
		upload_to=partial(maker, "users", keys=["email"]),
		max_length=255,
		blank=True,
		null=True,
	)
	products = models.ManyToManyField(Product, related_name="products", blank=True)
	products_manager = models.BooleanField(default=False)
	
	last_login = models.DateTimeField(
		auto_now=True, editable=False, blank=True, null=True
	)
	
	objects = UserManager()
	
	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ["email"]
	
	class Meta:
		indexes = [
			models.Index(fields=["username"]),
			models.Index(fields=["email"]),
		]


class Address(models.Model):
	address = models.CharField(max_length=200)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	zip_code = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	
	def __str__(self):
		return f"{self.address} {self.country} {self.city} {self.state} {self.zip_code}"


class Cart(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	product_id = models.ForeignKey("products.Product", on_delete=models.CASCADE)
	quantity = models.IntegerField()


class Order(models.Model):
	total_price = models.FloatField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	gift_card = models.IntegerField(null=True, blank=True)
	order_history = models.TextField(null=True, blank=True)
	order_mode = models.CharField(max_length=100, null=True, blank=True)
	order_items = models.ForeignKey(
		"OrderItems",
		blank=True,
		related_name="order_items",
		null=True,
		on_delete=models.CASCADE,
	)
	payment = models.ForeignKey(
		"buy.Payment",
		blank=True,
		related_name="payment",
		null=True,
		on_delete=models.CASCADE,
	)


class OrderItems(models.Model):
	product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
	quantity = models.IntegerField()
	price = models.FloatField()
	gift_card = models.IntegerField(null=True, blank=True)


class WishList(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	product = models.ForeignKey("products.Product", on_delete=models.CASCADE)


class Permission(models.Model):
	name = models.CharField(max_length=50)
	module = models.CharField(max_length=50)


class Role(models.Model):
	name = models.CharField(max_length=50)
	permissions = models.ManyToManyField(Permission)


class UserRole(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
