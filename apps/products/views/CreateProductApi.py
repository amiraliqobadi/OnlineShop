from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
)
from apps.products.forms import CreateProductForm
from apps.products.models import Product, ImageAlbum
from django.contrib import messages
from django.core.files.storage import default_storage
import json
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import F


class CreateProductView(CreateView):
    model = Product
    form_class = CreateProductForm
    template_name = "products/CreateProduct.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_name"] = self.request.user.username
        return context

    def dispatch(self, *args, **kwargs):
        if not self.request.user.products_manager:
            messages.error(self.request, "you dont have permission to do it")
            return redirect("home")
        else:
            messages.success(self.request, "welcome product manager")
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        images = form.cleaned_data["product_images"]
        images_list = list()
        for image in images:
            file_path = default_storage.save(image.name, ContentFile(image.read()))
            images_list.append(file_path)
        product_images = ImageAlbum.objects.create(images=json.dumps(images_list))
        form.instance.product_images = product_images
        form.instance.created_by = self.request.user.username

        if form.instance.discount_percent is not None:
            form.instance.price_after_discount_percent = (
                form.instance.price * form.instance.discount_percent
            ) / 100
        elif form.instance.discount is not None:
            form.instance.price_after_discount -= form.instance.discount

        form.save()
        return super().form_valid(form)


class JsonResponseMixin:
    def render_to_response(self, request, context, **response_kwargs):
        if self.request.is_ajax():
            return JsonResponse(context, safe=False, **response_kwargs)
        else:
            return super().render_to_response(context, **response_kwargs)
