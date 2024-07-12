from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import (
	ListView,
)

from apps.user.models import User


class ProductManagerProfile(ListView):
	template_name = "user/product_manager_dashboard.html"
	model = User
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user
		context["role"] = user.products_manager
		return context
	
	def dispatch(self, *args, **kwargs):
		if not self.request.user.products_manager:
			messages.error(self.request, "you dont have permission to do it")
			return redirect("home")
		else:
			messages.success(self.request, "welcome product manager")
		return super().dispatch(*args, **kwargs)
