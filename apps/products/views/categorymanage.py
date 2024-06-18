from apps.products.models import Category
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from apps.products.forms import CreateCategoryForm
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from apps.products.permissions import ProductsManager


class CategoryManager(ListView):
    model = Category
    template_name = "products/category_manage.html"

    def dispatch(self, *args, **kwargs):
        if not self.request.user.products_manager:
            messages.error(self.request, "you dont have permission to do it")
            return redirect("home")
        else:
            messages.success(self.request, "welcome product manager")
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}

        if not Category.objects.all():
            context["category"] = None
        else:
            context["category"] = Category.objects.all()
        return context


class CreateCategory(CreateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = "products/create_category.html"
    success_url = reverse_lazy("CategoryManager")

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
        form.instance.created_by = self.request.user.username
        form.save()
        return super().form_valid(form)


class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy("CategoryManager")
    permission_classes = [ProductsManager]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        category = self.get_object()
        category.is_active = False
        category.save()
        messages.success(request, "Category deleted successfully")
        return redirect(self.success_url)


class CategoryUpdateView(UpdateView):
    model = Category
    fields = [
        "name",
        "parent",
    ]
    template_name = "products/update_category.html"
    success_url = reverse_lazy("CategoryManager")

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs["pk"])
