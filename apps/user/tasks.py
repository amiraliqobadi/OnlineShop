from celery import shared_task
from apps.user.middleware import (
    VerifyUserMiddleware,
)  # Adjust the import path according to your project structure


@shared_task
def verify_users():
    middleware = VerifyUserMiddleware(None)
    middleware.__call__(None)
