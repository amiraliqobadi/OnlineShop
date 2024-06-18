from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Address, Order, OrderItems


User = get_user_model()


class UserModelTest(TestCase):
    def setUpTestData(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_user_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("user_name").verbose_name
        self.assertEqual(field_label, "user name")

    def test_user_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("user_name").max_length
        self.assertEqual(max_length, 50)

    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "email")

    def test_email_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("email").max_length
        self.assertEqual(max_length, 50)


class AddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Address.objects.create(
            address="123 Main St",
            city="Anytown",
            state="CA",
            zip_code="12345",
            country="USA",
        )

    def test_address_content(self):
        address = Address.objects.get(id=1)
        expected_object_name = f"{address.address}, {address.city}, {address.state}, {address.zip_code}, {address.country}"
        self.assertEqual(expected_object_name, "123 Main St, Anytown, CA, 12345, USA")


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Order.objects.create(total_price=100.00)

    def test_order_total_price(self):
        order = Order.objects.get(id=1)
        self.assertEqual(order.total_price, 100.00)


class OrderItemsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        OrderItems.objects.create(quantity=1, price=100.00)

    def test_order_items_quantity(self):
        order_item = OrderItems.objects.get(id=1)
        self.assertEqual(order_item.quantity, 1)

    def test_order_items_price(self):
        order_item = OrderItems.objects.get(id=1)
        self.assertEqual(order_item.price, 100.00)
