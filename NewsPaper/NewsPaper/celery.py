import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'News.tasks.del_task',
        'schedule': crontab(minute=0, hour='*/3'),
        'args': (5,),
    },
}

app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'News.tasks.send_subscribers_week',
        'schedule': crontab(minute='00', hour='21', day_of_week='fri'),
        'args': (5,),
    },
}

