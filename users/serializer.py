from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone

from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        # Получаем данные (токены и пользователя) от родителя
        data = super().validate(attrs)

        # Обновляем дату последнего входа
        self.user.last_login = timezone.now()
        self.user.save(update_fields=['last_login'])

        # Опционально: добавляем данные пользователя в ответ
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'last_login': self.user.last_login,
        }

        return data