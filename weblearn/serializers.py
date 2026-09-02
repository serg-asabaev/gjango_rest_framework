from rest_framework import serializers, viewsets

from users.models import Payment
from weblearn.models import LearnCourse, Lesson, Subscription
from weblearn.validators import LessonLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(validators=[LessonLinkValidator()])

    class Meta:
        model = Lesson
        fields = ("id", "title", "description", "learn_course", "video_link", "owner")


class LearnCourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson_list = LessonSerializer(source="lessons", many=True)
    subscribed = serializers.SerializerMethodField()

    class Meta:
        model = LearnCourse
        fields = ("id", "title", "description", "lesson_count", "lesson_list", "subscribed", "owner")

    def get_lesson_count(self, instance):
        lessons = instance.lessons.all()
        return lessons.count()

    def get_subscribed(self, instance):
        request = self.context.get('request')

        return Subscription.objects.filter(user=request.user, learn_course=instance).exists()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("user", "payment_time", "paid_course", "payment_sum", "payment_type")
