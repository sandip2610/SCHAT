from celery import shared_task
from django.utils import timezone
from .models import Status

@shared_task
def delete_expired_statuses():
    expired_statuses = Status.objects.filter(timestamp__lt=timezone.now() - timezone.timedelta(hours=24))
    expired_statuses.delete()