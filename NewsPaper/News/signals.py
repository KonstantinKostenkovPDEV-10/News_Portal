from django.db.models.signals import post_save
from django.dispatch import receiver # импортируем нужный декоратор
from .models import Post
import smtplib
from email.mime.text import MIMEText



# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Post)
def notify_managers_post(sender, instance, created, **kwargs):
    if created:
        subject = f'Новая статья на News Portal - {instance.title_news} {instance.date_time_create.strftime("%d %m %Y")}'
    else:
        subject = f'Статья была изменена {instance.title_news} {instance.date_time_create.strftime("%d %m %Y")}'
    send = "admin008@mail.ru"
    # your password = "your password"
    password = "5cqweYjVfiBBNPo2LyTZ"
    server = smtplib.SMTP("smtp.mail.ru", 25)
    server.starttls()

    try:
        server.login(send, password)
        msg = MIMEText(subject)
        msg["Subject"] = "CLICK ME PLEASE!"
        server.sendmail(send, send, msg.as_string())

        server.sendmail(send, send, f"Subject: CLICK ME PLEASE!\n{subject}")

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"

