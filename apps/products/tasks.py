from celery import shared_task
from datetime import datetime
from apps.products.models import Product


@shared_task
def check_and_remove_expired_discounts():
    # Query for products with expired discounts
    expired_products = Product.objects.filter(discount_expires_at__gte=datetime.now())

    # Update or delete expired products
    for product in expired_products:
        # Example: Set discount to 0
        product.discount_percent = 0
        product.discount = 0
        product.save()
