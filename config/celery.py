import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj.settings")
app = Celery("proj")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


CELERY_BEAT_SCHEDULE = {
    "verify-users-every-day": {
        "task": "apps.user.tasks.verify_users",
        "schedule": crontab(minute="0", hour="0"),
    },
}

app.conf.beat_schedule = {
    "check-expired-discounts": {
        "task": "apps.products.check_and_remove_expired_discounts",
        "schedule": crontab(minute="*/1"),
    },
}
