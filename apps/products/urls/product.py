from django.urls import path

from apps.products.views.category_manage import (
	CategoryManager,
	CreateCategory,
	CategoryDelete,
	CategoryUpdateView,
)
from apps.products.views.create_productApi import CreateProductView
from apps.products.views.manage_coupon import CouponManage, CreateCouponView, DeleteCoupon, UpdateCouponView
from apps.products.views.product_api import (
	ProductListCreateAPIView,
	CategoryView,
	ShowProduct,
)
from apps.products.views.product_manager import (
	ProductDeleteAPIView,
	ProductList,
	ProductUpdateView,
)

urlpatterns = [
	path("", ProductListCreateAPIView.as_view(), name="home"),
	path("create/product", CreateProductView.as_view(), name="create_product"),
	path(
		"delete/product/<int:pk>", ProductDeleteAPIView.as_view(), name="delete_product"
	),
	path("product/manage", ProductList.as_view(), name="product_list_manage"),
	path("<int:pk>/update_product", ProductUpdateView.as_view(), name="product_update"),
	path("category/<int:pk>", CategoryView.as_view(), name="category"),
	path("<int:pk>/show/product", ShowProduct.as_view(), name="ShowProduct"),
	path("category/manage", CategoryManager.as_view(), name="CategoryManager"),
	path("category/manage/create", CreateCategory.as_view(), name="CreateCategory"),
	path(
		"manage/category/delete/<int:pk>",
		CategoryDelete.as_view(),
		name="CategoryDelete",
	),
	path(
		"<int:pk>/update/category", CategoryUpdateView.as_view(), name="CategoryUpdate"
	),
	path("manage/coupon", CouponManage.as_view(), name="ManageCoupons"),
	path("manage/create/coupon", CreateCouponView.as_view(), name="CreateCoupon"),
	path("manage/delete/coupon/<int:pk>", DeleteCoupon.as_view(), name="DeleteCoupon"),
	path("<int:pk>/manage/update/coupon", UpdateCouponView.as_view(), name="UpdateCoupon"),
]
