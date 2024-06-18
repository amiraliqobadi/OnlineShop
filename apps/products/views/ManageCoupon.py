from apps.products.models import Coupon
from apps.user.models import User
from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    TemplateView,
)
from apps.products.forms import CreateCategoryForm
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from apps.products.forms import CreateCoupon


class CouponManage(ListView):
    template_name = "Coupons/manage_coupons.html"
    model = User

    def dispatch(self, *args, **kwargs):
        if not self.request.user.products_manager:
            messages.error(self.request, "you dont have permission to do it")
            return redirect("home")
        else:
            messages.success(self.request, "welcome product manager")
        return super().dispatch(*args, **kwargs)
