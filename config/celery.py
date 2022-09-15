import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {

       'send_email_newsletters_every_monday_8_time': {
        'task': 'newsportal.tasks.celery_news_letters_weekly',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args':()
    },

}
