from django.shortcuts import render
from rest_framework import viewsets, generics

from users.models import Payment
from weblearn.serializers import PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()