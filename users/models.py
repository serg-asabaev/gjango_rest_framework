from django.contrib.auth.models import (AbstractUser, PermissionsMixin,
                                        UserManager)
from django.db import models

from weblearn.models import LearnCourse


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Введите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите свой аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    is_staff = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    objects = UserManager()


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    payment_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")

    paid_course = models.ForeignKey(
        LearnCourse,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="payments",
        verbose_name="Оплаченный курс",
    )

    payment_sum = models.FloatField(verbose_name="Сумма оплаты")

    class PaymentType(models.TextChoices):
        CASH = "cash", "Наличные"
        ACCOUNT_TRANSFER = "account_transfer", "Перевод на счет"

    payment_type = models.CharField(
        max_length=16,
        choices=PaymentType.choices,
        default=PaymentType.CASH,
    )
