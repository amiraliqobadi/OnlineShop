from apps.user.models import User
from apps.user.forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from datetime import datetime
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
import random
import string
from django.conf import settings
from django.templatetags.static import static


class AuthUserView(View):
    template_name = "user/active.html"
    success_url = reverse_lazy("signin")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if "email" in request.POST:
            user_email = request.POST.get("email")
            verification_code = self.generate_verification_code()
            self.send_verification_code(user_email, verification_code)
            request.session["user_email"] = user_email
            request.session["verification_code"] = verification_code
            return render(
                request, self.template_name, {"show_verification_code_input": True}
            )
        elif "verification_code" in request.POST:
            verification_code = request.POST.get("verification_code")
            stored_code = request.session.get("verification_code")
            if verification_code == stored_code:
                user_email = request.session.get("user_email")
                try:
                    user = User.objects.get(email=user_email)
                    user.is_active = True
                    if "profile_img" in self.request.FILES:
                        User.profile_img = self.request.FILES["profile_img"]
                    else:
                        User.profile_img = static("default-avatar.png")
                    request.session["verified"] = True
                    user.save()
                    messages.success(request, "Account activated successfully!")
                except User.DoesNotExist:
                    messages.error(request, "User with this email does not exist.")
                return HttpResponseRedirect(self.success_url)
            else:
                messages.error(request, "Invalid verification code. Please try again.")
        return render(request, self.template_name)

    @staticmethod
    def generate_verification_code():
        return "".join(random.choices(string.digits, k=6))

    @staticmethod
    def send_verification_code(user_email, verification_code):
        subject = "Authentication code: Online Shop"
        message = f"Your authentication code is: {verification_code}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "user/signup.html"
    success_url = reverse_lazy("activate_account")

    def form_valid(self, form):
        User.is_active = False
        form.save(commit=False)
        return super().form_valid(form)


class SignInView(LoginView):
    template_name = "user/login.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Login successful. Welcome !")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("home")


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        User.last_login = datetime.now()
        redirect("signin")
        return super().dispatch(request, *args, **kwargs)
