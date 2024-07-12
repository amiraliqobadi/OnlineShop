from django.test import TestCase
from apps.core.models import LogicalMixin


class LogicalMixinTest(TestCase):
    def setUp(self):
        # Assuming YourModelName is a model that uses LogicalMixin
        self.instance = LogicalMixin.objects.create()

    def test_delete_method(self):
        # Test if the delete method sets is_deleted to True
        self.instance.delete()
        self.assertTrue(self.instance.is_deleted)

    def test_deactivate_method(self):
        # Test if the deactivate method sets is_active to False
        self.instance.deactivate()
        self.assertFalse(self.instance.is_active)
