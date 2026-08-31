from rest_framework import serializers, viewsets

from users.models import Payment
from weblearn.models import LearnCourse, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ("id", "title", "description", "learn_course")


class LearnCourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson_list = LessonSerializer(source="lessons", many=True)

    class Meta:
        model = LearnCourse
        fields = ("id", "title", "description", "lesson_count", "lesson_list")

    def get_lesson_count(self, instance):
        lessons = instance.lessons.all()
        return lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("user", "payment_time", "paid_course", "payment_sum", "payment_type")
