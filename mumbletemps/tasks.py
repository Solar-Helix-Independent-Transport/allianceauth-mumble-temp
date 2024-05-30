from celery import shared_task
import logging

import datetime

from .models import TempLink, TempUser

logger = logging.getLogger(__name__)


@shared_task
def tidy_up_temp_links():
    TempLink.objects.filter(
        expires__lt=datetime.datetime.utcnow()
        .replace(tzinfo=datetime.timezone.utc)
        .timestamp()
    ).delete()
    TempUser.objects.filter(templink__isnull=True).delete()
    TempUser.objects.filter(
        expires__lt=datetime.datetime.utcnow()
        .replace(tzinfo=datetime.timezone.utc)
        .timestamp()
    ).delete()
