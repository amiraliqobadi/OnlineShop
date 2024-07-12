# Create your tests here.
# Assuming this is in apps/core/tests.py or apps/product/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from apps.products.models import Product, Category, Comment, Like
from apps.products.managers import CommentManager, LogicalManager


class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            created_by="Admin",
            name="Test Product",
            price=100.00,
            quantity=10,
            brand="BrandX",
            category=self.category,
            description="A test product",
            stars=5,
            review_count=1,
            coupon=None,
            product_images=None,
        )

    def test_product_creation(self):
        self.assertEqual(self.product.created_by, "Admin")
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 100.00)
        self.assertEqual(self.product.quantity, 10)
        self.assertEqual(self.product.brand, "BrandX")
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.description, "A test product")
        self.assertEqual(self.product.stars, 5)
        self.assertEqual(self.product.review_count, 1)
        self.assertIsNone(self.product.coupon)
        self.assertIsNone(self.product.product_images)


class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Electronics")
        self.assertEqual(category.name, "Electronics")


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="commentuser", password="67890")
        self.product = Product.objects.create(
            created_by="Admin",
            name="Test Product",
            price=100.00,
            quantity=10,
            brand="BrandX",
            category=None,
            description="A test product",
            stars=5,
            review_count=1,
            coupon=None,
            product_images=None,
        )
        self.comment = Comment.objects.create(
            product=self.product, user=self.user, content="Great product!"
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.product, self.product)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.content, "Great product!")


class LikeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="likeluser", password="98765")
        self.product = Product.objects.create(
            created_by="Admin",
            name="Test Product",
            price=100.00,
            quantity=10,
            brand="BrandX",
            category=None,
            description="A test product",
            stars=5,
            review_count=1,
            coupon=None,
            product_images=None,
        )
        self.like = Like.objects.create(user=self.user, product=self.product)

    def test_like_creation(self):
        self.assertEqual(self.like.user, self.user)
        self.assertEqual(self.like.product, self.product)
