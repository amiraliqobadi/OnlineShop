from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from apps.user.views.api import SignUpView, SignInView, CustomLogoutView, AuthUserView
from apps.user.views.product_manager_profile import ProductManagerProfile
from apps.user.views.user_profile import Profile, UpdateUserInfo, DeleteUserApi

# from apps.user.views.cart import addtocart

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
	path("user/profile/<int:pk>/", Profile.as_view(), name="profile"),
	path("user/profile/update/<int:pk>/", UpdateUserInfo.as_view(), name="update_user_info"),
	path("user/profile/delete/<int:pk>/", DeleteUserApi.as_view(), name="delete_user_info"),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
