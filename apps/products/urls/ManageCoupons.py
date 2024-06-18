from django.urls import path
from apps.products.views.ManageCoupon import CouponManage

urlpatterns = [
    path("manage/coupons", CouponManage.as_view(), name="ManageCoupons"),
]
