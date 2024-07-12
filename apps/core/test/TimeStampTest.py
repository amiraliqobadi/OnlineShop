from django.test import TestCase
from django.utils import timezone
from apps.core.models import TimeStampMixin # Replace YourModelName with the actual name of your model


class TimeStampMixinTest(TestCase):
    def setUp(self):
        # Assuming YourModelName is a model that uses TimeStampMixin
        self.instance = TimeStampMixin.objects.create()

    def test_create_at_field(self):
        # Check if create_at field is set to the current time
        self.assertIsNotNone(self.instance.create_at)
        self.assertAlmostEqual(self.instance.create_at, timezone.now(), delta=timezone.timedelta(seconds=1))

    def test_modify_at_field(self):
        # Check if modify_at field is set to the current time
        self.assertIsNotNone(self.instance.modify_at)
        self.assertAlmostEqual(self.instance.modify_at, timezone.now(), delta=timezone.timedelta(seconds=1))



