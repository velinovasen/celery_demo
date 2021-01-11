from __future__ import absolute_import, unicode_literals    # PREVENTS FROM IMPORT COLLISION IN FUTURE (BIG PROBLEM)

import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_demo.settings')

app = Celery('celery_demo')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://localhost:6379/0'

app.conf.beat_schedule = {
    'every-1-minute': {
        'task': 'notifications.tasks.send_email',
        'schedule': crontab(minute='*/1'),
        'args': ('velinovasen@yahoo.com',)
    }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')