from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post, Category, PostCategory
import datetime
global _t
from .tasks import send_subscribers_change,send_subscribers_add


@receiver(m2m_changed, sender=Post.post_category.through)
def post_category_change(sender, instance, **kwargs):
    action = kwargs.pop('action', None)
    pk = kwargs.pop('pk_set', None)
    if action=='post_add':
        send_subscribers_add(instance, pk)

@receiver(post_save, sender=Post)
def post_get(sender, instance,created, **kwargs):
    if created:
        print('create_post -',instance.id)
    else:
        print('update_post -', instance.id)
        send_subscribers_change(instance)

def limit_post(sender, instance, **kwargs):
    count_posts = sender.objects.filter(author_id=instance.author_id, Post__date=datetime.datetime.now().date())
    print('количество статей', len(count_posts))
    return len(count_posts)
