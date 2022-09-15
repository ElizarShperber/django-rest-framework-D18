import datetime
import os
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Subscriber, Post
from .tasks import celery_send_email_subscribers


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers_add_news(sender, instance, **kwargs):
    categories = instance.category.all()
    print('all_categories', categories)

    for category in categories:

        print('category_selected', category)

        subscribers = Subscriber.objects.filter(category=category.id).values('user')
        print(subscribers, 'subscribers')

        for subscriber in subscribers:
            subscriber = subscriber.get('user', None)
            print(subscriber, 'id user / variable subscriber')

            # отправляем письмо

            user_subscriber_username = User.objects.get(pk=subscriber).username
            user_subscriber_email = User.objects.get(pk=subscriber).email
            print(user_subscriber_username, 'user_subscriber_username')
            print(user_subscriber_email, 'user_subscriber_email')

            html_content = render_to_string(
                'letter_to_subscribers_news_created.html',
                {
                    'new_post': instance,
                    'username': user_subscriber_username,
                }
            )
            if user_subscriber_email:
                celery_send_email_subscribers.delay(
                    subject=f'{instance.title} ',
                    from_email=os.getenv('EMAIL_FROM'),
                    email=user_subscriber_email,
                    html_content=html_content)


@receiver(pre_save, sender=Post)
def check_post_author_by_date(sender, instance, **kwargs):
    print('check post author')
    quantity_posts = sender.objects.filter(author=instance.author,
                                           date_time_create__date=datetime.datetime.now().date())
    print('количество статей', len(quantity_posts))

    if len(quantity_posts) < 4:
        return len(quantity_posts)
    else:
        return
