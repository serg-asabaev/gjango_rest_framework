from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from .models import LearnCourse, Subscription
from users.models import User

@shared_task
def send_course_update_email(learn_course_id: int):
    from_email = 'usr123qwe@yandex.ru'
    learn_course = LearnCourse.objects.get(id=learn_course_id)

    subject = f'Обновление материалов курса'
    message = f'Обновились материалы по курсу {learn_course.title}, заходите чтобы просмотреть изменения!'
    recipient_list = []
    subs_list = Subscription.objects.filter(learn_course=learn_course)

    for subs in subs_list:
        recipient_list.append(subs.user.email)

    try:
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, connection=None)
    finally:
        print('all messages recieved!')


@shared_task
def check_user_last_login():
    users = User.objects.all()

    for user in users:
        now = timezone.now()
        date_delta = now - user.last_login
        if date_delta.days >= 30:
            user.is_active = False
            user.save()
