import json
import os

from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView
from rest_framework import generics

from apps.products.forms import UpdateProductForm
from apps.products.models import Product, ImageAlbum
from apps.products.permissions import ProductsManager
from apps.products.serializers.show_products_serializer import ProductSerializer


class ProductList(generics.ListAPIView):
	serializer_class = ProductSerializer
	permission_classes = [ProductsManager]
	templates = "products/product_manager.html"
	
	def get_queryset(self):
		return Product.objects.filter(is_active=True)
	
	def get_context_data(self, **kwargs):
		context = {}
		queryset = self.get_queryset()
		if queryset.exists():
			for pro in queryset:
				product = pro
				context["products"] = queryset
				context["price"] = product.price
				if product.price_after_discount is not None:
					context["price_after_discount"] = product.price_after_discount
					context["price_after_discount_percent"] = None
				elif product.price_after_discount_percent is not None:
					context[
						"price_after_discount_percent"
					] = product.price_after_discount_percent
					context["price_after_discount_percent"] = None
				context["name"] = product.name
				context["is_active"] = product.is_active
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(request, self.templates, context)


class ProductDeleteAPIView(DeleteView):
	model = Product
	success_url = reverse_lazy("product_list_manage")
	permission_classes = [ProductsManager]
	
	def dispatch(self, *args, **kwargs):
		if not self.request.user.products_manager:
			messages.error(self.request, "you dont have permission to do it")
			return redirect("home")
		else:
			messages.success(self.request, "welcome product manager")
		return super().dispatch(*args, **kwargs)
	
	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(pk=self.kwargs["pk"])
	
	def post(self, request, *args, **kwargs):
		product = self.get_object()
		product.is_active = False
		product.save()
		messages.success(request, "Product deleted successfully")
		return redirect(self.success_url)


class ProductUpdateView(UpdateView):
	model = Product
	form_class = UpdateProductForm
	template_name_suffix = "_update_form"
	success_url = reverse_lazy("product_list_manage")
	
	def dispatch(self, *args, **kwargs):
		if not self.request.user.products_manager:
			messages.error(self.request, "you dont have permission to do it")
			return redirect("home")
		else:
			messages.success(self.request, "welcome product manager")
		return super().dispatch(*args, **kwargs)
	
	def form_valid(self, form):
		if form.cleaned_data.get("product_images"):
			product = self.object
			if product.product_images:
				old_images = json.loads(product.product_images.images)
				for image_path in old_images:
					if os.path.exists(image_path):
						os.remove(image_path)
			new_images = form.cleaned_data["product_images"]
			images_list = []
			for image in new_images:
				file_path = default_storage.save(image.name, ContentFile(image.read()))
				images_list.append(file_path)
			product_images = ImageAlbum.objects.create(images=json.dumps(images_list))
			product.product_images = product_images
			product.save()
		
		messages.success(self.request, "Your information has been updated successfully")
		return super().form_valid(form)
