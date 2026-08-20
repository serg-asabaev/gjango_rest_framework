from rest_framework import serializers

from users.models import Payment
from weblearn.models import LearnCourse, Lesson

class LearnCourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson_list = serializers.SerializerMethodField()

    class Meta:
        model = LearnCourse
        fields = ('id', 'title', 'description', 'lesson_count', 'lesson_list')

    def get_lesson_count(self, instance):
        lessons = instance.lessons.all()
        return lessons.count()

    def get_lesson_list(self, instance):
        lessons = instance.lessons.all()
        lessons_list = []
        for lesson in lessons:
            lessons_list.append({
                "title": f"{lesson.title}",
                "description": f"{lesson.description}"
            })
        return lessons_list

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'learn_course')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('user', 'payment_time', 'paid_course', 'payment_sum', 'payment_type')