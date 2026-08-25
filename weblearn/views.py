from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from weblearn.serializers import LearnCourseSerializer, LessonSerializer#, LearnCourseLessonSerializer
from weblearn.models import LearnCourse, Lesson
from weblearn.permissions import IsOwnerOrStaff

class LearnCourseViewSet(viewsets.ModelViewSet):
    serializer_class = LearnCourseSerializer
    queryset = LearnCourse.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_learn_course = serializer.save()
        new_learn_course.owner = self.request.user
        new_learn_course.save()

class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

# class LearnCourseLessonListAPIView(generics.ListAPIView):
#     queryset = Lesson.objects.filter(learn_course__isnull=False)
#     serializer_class = LearnCourseLessonSerializer