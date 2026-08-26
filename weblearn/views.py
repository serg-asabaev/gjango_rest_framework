from rest_framework import generics, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from weblearn.models import LearnCourse, Lesson
from weblearn.permissions import IsOwner, IsManager
from weblearn.serializers import (  # , LearnCourseLessonSerializer
    LearnCourseSerializer, LessonSerializer)


class LearnCourseViewSet(viewsets.ModelViewSet):
    queryset = LearnCourse.objects.all()
    serializer_class = LearnCourseSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsManager, ]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsManager | IsOwner, ]
        elif self.action in ["destroy"]:
            self.permission_classes = [~IsManager, IsOwner,]
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsManager, IsAuthenticated]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsManager | IsOwner]

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsManager | IsOwner]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsManager | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, ~IsManager]


# class LearnCourseLessonListAPIView(generics.ListAPIView):
#     queryset = Lesson.objects.filter(learn_course__isnull=False)
#     serializer_class = LearnCourseLessonSerializer
