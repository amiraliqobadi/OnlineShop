from django.utils import timezone
from django.db.models import Q
from apps.user.models import User


class VerifyUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.session.get("verified", False) is False:
            users_to_remove = User.objects.filter(
                Q(is_active=True)
                & Q(created_at__lt=timezone.now() - timezone.timedelta(days=3))
            )
            for user in users_to_remove:
                user.delete()
        return self.get_response(request)
