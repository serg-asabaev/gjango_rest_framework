from django.core.management import BaseCommand

from users.models import User, Payment
from weblearn.models import LearnCourse


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.get(id=1)
        payment = Payment.objects.create(user=user, payment_sum=100000)
        payment.payment_type = payment.PaymentType.CASH
        payment.paid_course = LearnCourse.objects.get(id=1)
        payment.save()