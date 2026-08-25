from rest_framework import viewsets, generics

from weblearn.serializers import LearnCourseSerializer, LessonSerializer#, LearnCourseLessonSerializer
from weblearn.models import LearnCourse, Lesson


class LearnCourseViewSet(viewsets.ModelViewSet):
    serializer_class = LearnCourseSerializer
    queryset = LearnCourse.objects.all()

class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()

# class LearnCourseLessonListAPIView(generics.ListAPIView):
#     queryset = Lesson.objects.filter(learn_course__isnull=False)
#     serializer_class = LearnCourseLessonSerializer