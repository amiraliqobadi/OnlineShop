from django.db import models

from apps.core.managers import LogicalManager
from apps.core.models import TimeStampMixin, LogicalMixin
from .managers import CommentManager


class Coupon(models.Model):
	created_date = models.DateTimeField(auto_now=True, editable=True)
	expire_date = models.DateTimeField(auto_now_add=True, editable=True)
	code = models.CharField(max_length=50, unique=True)
	percent_discount = models.FloatField()
	price_discount = models.FloatField()
	capacity = models.IntegerField(default=0)


class ImageAlbum(models.Model):
	images = models.TextField()


class Product(TimeStampMixin, LogicalMixin):
	created_by = models.CharField(max_length=255)
	price_discount = models.IntegerField(default=0, null=True, blank=True)
	percent_discount = models.IntegerField(default=0, null=True, blank=True)
	name = models.CharField(max_length=255)
	price = models.FloatField()
	quantity = models.IntegerField()
	brand = models.CharField(max_length=255)
	category_id = models.ForeignKey(
		"Category",
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	description = models.CharField(max_length=255)
	stars = models.IntegerField(default=0)
	review_count = models.IntegerField(default=0, null=True, blank=True)
	product_images = models.ForeignKey(
		ImageAlbum,
		on_delete=models.CASCADE,
		related_name="product_images",
	)
	discount_percent = models.FloatField(null=True, blank=True)
	price_after_discount_percent = models.FloatField(
		null=True, blank=True, default=None
	)
	discount = models.FloatField(null=True, blank=True)
	price_after_discount = models.FloatField(null=True, blank=True, default=None)
	discount_expires_at = models.DateTimeField(null=True, blank=True)
	
	def save(self, *args, **kwargs):
		if self.discount_expires_at:
			if not self.discount:
				self.discount = 0
		super().save(*args, **kwargs)


class Like(TimeStampMixin, LogicalMixin):
	user_id = models.ForeignKey(
		"user.User", on_delete=models.CASCADE, related_name="likes"
	)
	product_id = models.ForeignKey(
		"Product", on_delete=models.CASCADE, related_name="likes"
	)
	
	class Meta:
		unique_together = ("user_id", "product_id")


class Category(TimeStampMixin, LogicalMixin):
	name = models.CharField(max_length=255)
	parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
	
	def __str__(self):
		return self.name


class Comment(TimeStampMixin, LogicalMixin):
	product_id = models.ForeignKey(
		"Product", on_delete=models.CASCADE, related_name="comments"
	)
	user = models.ForeignKey(
		"user.User", on_delete=models.CASCADE, related_name="comments"
	)
	reply = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
	content = models.TextField()
	
	objects = CommentManager()
	custom = LogicalManager()
	
	class Meta:
		unique_together = ("product_id", "user", "reply")
	
	@property
	def replies(self):
		return self.comment_set(manager="custom")
