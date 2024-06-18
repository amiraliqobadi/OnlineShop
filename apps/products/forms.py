from django import forms
from apps.products.models import Product, Category, Coupon
from multiupload.fields import MultiFileField


class CreateProductForm(forms.ModelForm):
    product_images = MultiFileField(min_num=1, max_num=5, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category_id"].queryset = Category.objects.filter(is_active=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "quantity",
            "brand",
            "category_id",
            "description",
            "discount_percent",
            "discount",
            "discount_expires_at",
        ]
        widgets = {
            "discount_expires_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }


class UpdateProductForm(CreateProductForm):
    pass


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "name",
            "parent",
        ]


class CreateCoupon(forms.ModelForm):
    class Meta:
        Model = Coupon
        fields = [
            "expire_date",
            "code",
            "percent_discount",
            "price_discount",
            "capacity",
        ]
