from django import forms
from multiupload.fields import MultiFileField

from apps.products.models import Product, Category, Coupon


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
	DISCOUNT_CHOICES = (
		('percent', 'Percent Discount'),
		('fixed_price', 'Price Discount'),
	)
	
	discount_type = forms.ChoiceField(choices=DISCOUNT_CHOICES)
	
	class Meta:
		model = Coupon
		fields = [
			"expire_date",
			"code",
			"discount_type",
			"capacity",
			"percent_discount",
			"price_discount",
		]
		widgets = {
			"expire_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
		}
		exclude = ['expire_date']
	
	def clean(self):
		cleaned_data = super().clean()
		discount_type = cleaned_data.get('discount_type')
		if discount_type == 'percent':
			self.fields['price_discount'].required = False
			self.fields['percent_discount'].required = True
		elif discount_type == 'fixed_price':
			self.fields['percent_discount'].required = False
			self.fields['price_discount'].required = True
		else:
			raise forms.ValidationError("Invalid discount type selected.")


class UpdateCoupon(CreateCoupon):
	pass
