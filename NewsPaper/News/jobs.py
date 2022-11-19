import datetime
import logging

from django.contrib.auth.models import User
from .models import Post, Category, Subscribers, PostCategory
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from email.mime.text import MIMEText


logger = logging.getLogger(__name__)

def my_job():
    time_delta = datetime.timedelta(7)
    start_date = datetime.datetime.utcnow() - time_delta
    end_date = datetime.datetime.utcnow()

    posts = Post.objects.filter(date_time_create__range=(start_date, end_date))

    for category in Category.objects.all():
        html_content = render_to_string('week_email.html',
                                        {'posts': posts, 'category': category}, )
        msg = EmailMultiAlternatives(
            subject=f'"Еженедельная подписка"',
            body="Новости",
            from_email='admin008@mail.ru',
            to=category.get_subscribers_emails())
        msg.attach_alternative(html_content, "text/html")
        msg.send()





def job_scheduler():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_job(my_job, 'cron', day_of_week='fri', hour=21,id='my_job_id')
    logger.info("Added job 'my_job'.")
    logger.info("Starting scheduler...")
    scheduler.start()
