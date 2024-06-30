import base64

from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework.generics import RetrieveAPIView, get_object_or_404, UpdateAPIView, DestroyAPIView
from rest_framework.renderers import TemplateHTMLRenderer

from apps.user.models import User
from apps.user.serializers import UserSerializer


class Profile(RetrieveAPIView):
	model = User
	serializer_class = UserSerializer
	templates = "user/user_profile.html"
	
	def get_queryset(self):
		return get_object_or_404(User, pk=self.kwargs['pk'])
	
	def dispatch(self, request, *args, **kwargs):
		if not self.kwargs['pk']:
			messages.error(request, "You must login")
			return redirect("home")
		context = self.get_context_data(**kwargs)
		if self.get_queryset().is_deleted or self.get_queryset().is_active is False:
			messages.error(request, "User not found")
			return redirect("signup")
		return render(request, self.templates, context)
	
	def get_context_data(self, **kwargs):
		context = {}
		queryset = self.get_queryset()
		context["user_name"] = queryset.username
		context["user_email"] = queryset.email
		context["f_name"] = queryset.f_name
		context["l_name"] = queryset.l_name
		if queryset.addresses is not None:
			for address in queryset.addresses:
				context["address"] = address.address
				context["city"] = address.city
				context["state"] = address.state
				context["zip_code"] = address.zip_code
				context["country"] = address.country
		else:
			context["address"] = None
			context["city"] = None
			context["state"] = None
			context["zip_code"] = None
			context["country"] = None
		
		if queryset.user_image is not None:
			context["user_img"] = queryset.user_image
		else:
			context["user_img"] = None
		return context
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(request, self.templates, context)


class UpdateUserInfo(UpdateAPIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'user/update_user_info.html'
	model = User
	serializer_class = UserSerializer
	
	def get(self, request, *args, **kwargs):
		user = get_object_or_404(User, pk=kwargs.get('pk'))
		serializer = self.serializer_class(user)
		return render(request, self.template_name, {'serializer': serializer})
	
	def post(self, request, *args, **kwargs):
		user = get_object_or_404(User, pk=kwargs.get('pk'))
		serializer = self.serializer_class(user, data=request.data)
		
		if serializer.is_valid():
			
			if serializer.validated_data.get('user_image'):
				serializer.save()
				image_base64 = base64.b64encode(serializer.validated_data['user_image'].read()).decode('utf-8')
				user.user_image = image_base64
				user.save()
			if serializer.validated_data.get('password'):
				user.set_password(serializer.validated_data['password'])
				return redirect('signin')
			
			serializer.save()
			messages.success(request, "User information updated successfully.")
			return render(request, self.template_name, {'serializer': serializer})
		else:
			return render(request, self.template_name, {'serializer': serializer})


class DeleteUserApi(DestroyAPIView):
	model = User
	
	def post(self, request, *args, **kwargs):
		user = get_object_or_404(User, pk=kwargs.get('pk'))
		user.delete()
		return redirect('signin')
