from rest_framework import viewsets

from weblearn.serializers import LearnCourseSerializer
from weblearn.models import LearnCourse

class LearnCourseViewSet(viewsets.ModelViewSet):
    serializer_class = LearnCourseSerializer
    queryset = LearnCourse.objects.all()
