from rest_framework import serializers

from weblearn.models import LearnCourse, Lesson

class LearnCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnCourse
        fields = ('title', 'description')