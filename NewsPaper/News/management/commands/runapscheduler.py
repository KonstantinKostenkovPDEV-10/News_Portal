import datetime
import logging

from django.contrib.auth.models import User
from django_apscheduler.models import DjangoJobExecution
from NewsPaper.News.models import Post, Category
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.management.base import BaseCommand
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
                                        {'posts': posts, 'category': category},)
        msg = EmailMultiAlternatives(
            subject=f'"Еженедельная подписка"',
            body="Новости",
            from_email='admin008@mail.ru',
            to=category.get_subscribers_emails())
        msg.attach_alternative(html_content, "text/html")
        msg.send()



def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(my_job,
                          trigger=CronTrigger(minutes=3),
                          id="my_job",
                          max_instances=100,
                          replace_existing=True,
                          # )

                          )


        #scheduler.add_job(
        #   my_job,
        #    trigger=CronTrigger(day="*/7"),
        #    id="my_job",
        #    max_instances=1,
        #    replace_existing=True,
       # )
        logger.info("Added job 'my_job'.")

       # scheduler.add_job(
        #    delete_old_job_executions,
        #   trigger=CronTrigger(
         #       day_of_week="fri", hour="22", minute="29"
       #    ),

       #     id="delete_old_job_executions",
       #     max_instances=1,
        #    replace_existing=True,
      #  )

        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")