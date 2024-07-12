from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from apps.buy.models import Payment, Shipment
from apps.user.models import Order


class PaymentModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="testuser", password="12345")
		self.order = Order.objects.create(
			user=self.user,
			order_date=datetime.now(),
			total_price=100.00,
			status="Pending",
		)
	
	def test_payment_creation(self):
		payment = Payment.objects.create(
			payment_id="123456",
			payment_status=True,
			payment_amount="100.00",
			payment_method="Credit Card",
			user=self.user,
		)
		self.assertEqual(payment.payment_id, "123456")
		self.assertTrue(payment.payment_status)
		self.assertEqual(payment.payment_amount, "100.00")
		self.assertEqual(payment.payment_method, "Credit Card")
		self.assertEqual(payment.user, self.user)
	
	def test_shipment_creation(self):
		shipment = Shipment.objects.create(
			shipment_id="789012",
			shipment_status=True,
			shipment_method="Standard Shipping",
			user=self.user,
			order=self.order,
		)
		self.assertEqual(shipment.shipment_id, "789012")
		self.assertTrue(shipment.shipment_status)
		self.assertEqual(shipment.shipment_method, "Standard Shipping")
		self.assertEqual(shipment.user, self.user)
		self.assertEqual(shipment.order, self.order)


class ShipmentModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="testuser2", password="67890")
		self.order = Order.objects.create(
			user=self.user,
			order_date=datetime.now(),
			total_price=100.00,
			status="Pending",
		)
	
	def test_shipment_creation_with_order(self):
		shipment = Shipment.objects.create(
			shipment_id="345678",
			shipment_status=True,
			shipment_method="Express Shipping",
			user=self.user,
			order=self.order,
		)
		self.assertEqual(shipment.shipment_id, "345678")
		self.assertTrue(shipment.shipment_status)
		self.assertEqual(shipment.shipment_method, "Express Shipping")
		self.assertEqual(shipment.user, self.user)
		self.assertEqual(shipment.order, self.order)
