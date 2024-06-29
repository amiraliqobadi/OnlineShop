import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import (
	ListView,
	DeleteView,
)
from django.views.generic.edit import UpdateView

from apps.products.forms import CreateCoupon
from apps.products.models import Coupon


class CouponManage(ListView):
	template_name = "Coupons/manage_coupons.html"
	model = Coupon
	queryset = Coupon.objects.all()
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		for coupon in self.queryset:
			context["count"] = len(list(Coupon.objects.all()))
			context["coupons"] = Coupon.objects.all()
			context["name"] = coupon.code
			context["expire_date"] = coupon.expire_date
			context["created_date"] = coupon.created_date
			context["price_discount"] = coupon.price_discount
			context["percent_discount"] = coupon.percent_discount
			context["capacity"] = coupon.capacity
		return context
	
	def dispatch(self, *args, **kwargs):
		if not self.request.user.products_manager:
			messages.error(self.request, "you dont have permission to do it")
			return redirect("home")
		else:
			messages.success(self.request, "welcome product manager")
		return super().dispatch(*args, **kwargs)


class CreateCouponView(CreateView):
	template_name = "Coupons/create_coupon.html"
	form_class = CreateCoupon
	success_url = reverse_lazy("ManageCoupon")
	
	def post(self, request, *args, **kwargs):
		form = self.form_class(data=request.POST)
		form.created_date = datetime.datetime.now()
		if form.is_valid():
			form.save()
			return redirect("ManageCoupon")
		else:
			return super().post(request, *args, **kwargs)
	
	def dispatch(self, *args, **kwargs):
		if not self.request.user.products_manager:
			messages.error(self.request, "you dont have permission to do it")
			return redirect("home")
		else:
			messages.success(self.request, "welcome product manager")
		return super().dispatch(*args, **kwargs)


class DeleteCoupon(DeleteView):
	model = Coupon
	success_url = reverse_lazy("ManageCoupon")
	
	def get_queryset(self):
		return Coupon.objects.filter(pk=self.kwargs["pk"])
	
	def post(self, request, *args, **kwargs):
		if self.get_queryset() is not None:
			self.get_queryset().delete()
			messages.success(request, f"coupon deleted successfully")
			return redirect(self.success_url)
		messages.error(request, "coupon not found")
		return redirect(self.success_url)


class UpdateCouponView(UpdateView):
	model = Coupon
	form_class = CreateCoupon
	queryset = Coupon.objects.all()
	success_url = reverse_lazy("ManageCoupon")
	template_name = "Coupons/Update_Coupon.html"
	
	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		return get_object_or_404(Coupon, pk=obj.pk)
	
	def form_valid(self, form):
		instance = self.get_object()
		form.instance = instance
		if form.is_valid():
			if form.cleaned_data['expire_date'] != instance.expire_date:
				form.instance.expire_date = form.cleaned_data['expire_date']
			if form.cleaned_data['code'] != instance.code:
				form.instance.code = form.cleaned_data['code']
			if form.cleaned_data['capacity'] != instance.capacity:
				form.instance.capacity = form.cleaned_data['capacity']
			if form.cleaned_data['percent_discount'] != instance.percent_discount:
				form.instance.percent_discount = form.cleaned_data['percent_discount']
			if form.cleaned_data['price_discount'] != instance.price_discount:
				form.instance.price_discount = form.cleaned_data['price_discount']
			form.instance.save()
			return HttpResponseRedirect(self.success_url)
		else:
			return render(self.request, self.template_name, {'form': form})
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['coupon'] = self.object
		return context
