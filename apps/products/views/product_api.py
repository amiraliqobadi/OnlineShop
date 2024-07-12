import json
from math import floor

from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import generics

from apps.products.models import Product, Category
from apps.products.serializers.show_products_serializer import ProductSerializer


class ProductListCreateAPIView(generics.ListAPIView):
	serializer_class = ProductSerializer
	templates = "products/product.html"
	
	def get_queryset(self):
		return Product.objects.filter(is_active=True)
	
	def get_context_data(self, **kwargs):
		context = {}
		queryset = self.get_queryset()
		if self.request.user.is_authenticated:
			context["product_manager"] = self.request.user.products_manager
		if not Category.objects.all():
			context["category"] = None
		else:
			context["category"] = Category.objects.all()
		if queryset.exists():
			for pro in queryset:
				product = pro
				images_list = json.loads(product.product_images.images)
				context["products"] = queryset
				context["images"] = images_list
				context["images_counter"] = len(images_list)
				context["name"] = product.name
				if product.price_after_discount is not None:
					context["price_after_discount"] = product.price_after_discount
					context["price_after_discount_percent"] = None
				elif product.price_after_discount_percent is not None:
					context[
						"price_after_discount_percent"
					] = product.price_after_discount_percent
					context["price_after_discount_percent"] = None
				context["price"] = product.price
				context["brand"] = product.brand
				context["is_active"] = product.is_active
				
				stars = list()
				counter = 0
				
				for s in range(int(product.stars)):
					counter += 1
				
				for s in range(floor(counter / 10)):
					stars.append("s")
				
				context["stars"] = stars
				context["star_counter"] = counter / 10
		
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(request, self.templates, context)


class CategoryView(ListView):
	model = Category
	template_name = "products/category.html"
	
	def get_queryset(self):
		category_id = self.kwargs.get("pk")
		if category_id is not None:
			return Product.objects.filter(category_id=category_id, is_active=True)
		else:
			return Product.objects.none()
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		queryset = self.get_queryset()
		if queryset.exists():
			for pro in queryset:
				product = pro
				images_list = json.loads(product.product_images.images)
				context["products"] = queryset
				context["images"] = images_list
				context["images_counter"] = len(images_list)
				context["name"] = product.name
				if product.price_after_discount is not None:
					context["price_after_discount"] = product.price_after_discount
					context["price_after_discount_percent"] = None
				elif product.price_after_discount_percent is not None:
					context[
						"price_after_discount_percent"
					] = product.price_after_discount_percent
					context["price_after_discount_percent"] = None
				context["price"] = product.price
				context["brand"] = product.brand
				context["is_deleted"] = product.is_deleted
			
			stars = list()
			counter = 0
			
			for s in range(int(product.stars)):
				counter += 1
			
			for s in range(floor(counter / 10)):
				stars.append("s")
			
			context["stars"] = stars
			context["star_counter"] = counter / 10
		return context


class ShowProduct(ListView):
	template_name = "products/show_product.html"
	model = Product
	
	def get_queryset(self, *, object_list=None, **kwargs):
		product_id = self.kwargs.get("pk")
		if product_id is not None:
			return Product.objects.filter(id=product_id).first()
		else:
			return Product.objects.none()
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		queryset = self.get_queryset()
		product = queryset
		images_list = json.loads(product.product_images.images)
		context["products"] = queryset
		context["images"] = images_list
		context["images_counter"] = len(images_list)
		context["name"] = product.name
		context["price"] = product.price
		if product.price_after_discount is not None:
			context["price_after_discount"] = product.price_after_discount
			context["price_after_discount_percent"] = None
		elif product.price_after_discount_percent is not None:
			context[
				"price_after_discount_percent"
			] = product.price_after_discount_percent
			context["price_after_discount_percent"] = None
		context["brand"] = product.brand
		context["is_deleted"] = product.is_deleted
		
		stars = list()
		counter = 0
		
		for s in range(int(product.stars)):
			counter += 1
		
		for s in range(floor(counter / 10)):
			stars.append("s")
		
		context["stars"] = stars
		context["star_counter"] = counter / 10
		
		return context
