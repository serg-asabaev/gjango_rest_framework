from rest_framework import serializers

from weblearn.models import LearnCourse, Lesson

class LearnCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnCourse
        fields = ('title', 'description')

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title', 'description')