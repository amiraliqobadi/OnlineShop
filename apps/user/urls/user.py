from django.urls import path
from apps.user.views.api import SignUpView, SignInView, CustomLogoutView, AuthUserView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from apps.user.views.Profile import ProductManagerProfile


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path(
        "Manager/product/",
        ProductManagerProfile.as_view(),
        name="ProductManagerProfile",
    ),
    path("activate/", AuthUserView.as_view(), name="activate_account"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
