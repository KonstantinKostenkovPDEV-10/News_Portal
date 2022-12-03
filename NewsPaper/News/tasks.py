import datetime
from celery import shared_task, Celery
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import PostCategory, Category, Post
from celery import shared_task


@shared_task
def send_subscribers_change(instance):
    url_title = f"http://127.0.0.1:8000/post/"
    subject = f'Статья была изменена - {instance.title_news} {instance.date_time_create.strftime("%d %m %Y")} {url_title}{instance.id}'
    _temp = PostCategory.objects.filter(post_id=instance.id).values('category_id')
    _t = _temp.values_list('category_id')
    _dict = _t[0]
    _category = Category.objects.get(id=_dict[0])
    msg = EmailMultiAlternatives(
        subject=f'"Еженедельная подписка"',
        body=subject,
        from_email='admin008@mail.ru',
        to=_category.get_subscribers_emails())
    msg.send()

@shared_task
def send_subscribers_add(instance,pk):
    url_title = f"http://127.0.0.1:8000/post/"
    subject = f'Новая статья на News Portal - {instance.title_news} {instance.date_time_create.strftime("%d %m %Y")} {url_title}{instance.id}'
    for p in pk: _t = p
    _category = Category.objects.get(id=_t)
    msg = EmailMultiAlternatives(
        subject=f'"Еженедельная подписка"',
        body=subject,
        from_email='admin008@mail.ru',
        to=_category.get_subscribers_emails())
    msg.send()

@shared_task
def send_subscribers_week():
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

@shared_task
def del_task():
    Celery.control.purge()

