import datetime
import os

from celery import shared_task
import time

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from newsportal.models import Subscriber, Post, Category


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
def celery_send_email_subscribers(subject, from_email, email, html_content):
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email = from_email,
        to=[email],
    )
    msg.attach_alternative(html_content,'text/html')
    msg.send()

@shared_task
def celery_news_letters_weekly():

    print('задача на еженедельную отправку')


    # получить список статей на отправку и сформировать письмо
    time_delta = datetime.timedelta(7)
    start_date = datetime.datetime.utcnow() - time_delta
    end_date = datetime.datetime.utcnow()

    posts = Post.objects.filter(date_time_create__range=(start_date, end_date))

    for category in Category.objects.all():
        html_content = render_to_string('account/email/week_email.html',
                                        {'posts': posts, 'category': category},)
        msg = EmailMultiAlternatives(
            subject=f'"Еженедельная подписка"',
            body="Новости и статьи",
            from_email=os.getenv('EMAIL_FROM'),
            to=category.get_subscribers_emails())
        msg.attach_alternative(html_content, "text/html")
        msg.send()

