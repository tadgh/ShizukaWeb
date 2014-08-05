import os
import celery
from django.conf import settings
from .server_poller import ServerPoller

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "ShizukaWeb.settings")

app = celery.Celery('ShizukaWeb')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))