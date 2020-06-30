from celery import shared_task
import logging

import datetime
from django.utils import timezone

from .models import TempLink, TempUser

logger = logging.getLogger(__name__)

# Create your tasks here

@shared_task
def tidy_up_temp_links():
    TempLink.objects.filter(expires__lt=datetime.datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()).delete()
    TempUser.objects.filter(templink__isnull=True).delete()
    TempUser.objects.filter(expires__lt=datetime.datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()).delete()