import os
from celery import Celery

#set default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

#create celery app instance
app = Celery('alx_travel_app')

#load task from all installed apps
app.config_from_object('django.conf:settings', namespace='CELERY')

#autodiscover tasks in all installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')