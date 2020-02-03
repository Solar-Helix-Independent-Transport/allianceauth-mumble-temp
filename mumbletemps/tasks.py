from celery import shared_task
import logging


logger = logging.getLogger(__name__)

# Create your tasks here

@shared_task
def tidy_up_temp_links():
    pass #do stuff
   