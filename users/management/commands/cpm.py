from django.core.management import BaseCommand

from users.models import User, Payment
from weblearn.models import LearnCourse


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.get(id=1)
        payment = Payment.objects.create(user=user, payment_sum=150000)
        payment.payment_type = payment.PaymentType.ACCOUNT_TRANSFER
        payment.paid_course = LearnCourse.objects.get(id=2)
        payment.save()