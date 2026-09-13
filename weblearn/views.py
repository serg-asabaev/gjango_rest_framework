from rest_framework import generics, viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import transaction

from weblearn.models import LearnCourse, Lesson, Subscription
from weblearn.permissions import IsOwner, IsManager
from weblearn.serializers import (  # , LearnCourseLessonSerializer
    LearnCourseSerializer, LessonSerializer)
from weblearn.paginators import LearnCoursePagination, LessonPagination
from weblearn.tasks import send_course_update_email


class LearnCourseViewSet(viewsets.ModelViewSet):
    queryset = LearnCourse.objects.all()
    serializer_class = LearnCourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LearnCoursePagination

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated] #[~IsManager, ]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsManager | IsOwner, ]
        elif self.action in ["destroy"]:
            self.permission_classes = [~IsManager, IsOwner,]
        return super().get_permissions()

    def get(self, request):
        queryset = LearnCourse.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LearnCourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_update(self, serializer):
        learn_course = serializer.save()
        transaction.on_commit(
            lambda: send_course_update_email.delay(learn_course.id)
        )


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
    pagination_class = LessonPagination
    permission_classes = [IsManager | IsOwner]

    def get(self, request):
        queryset = Lesson.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

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
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsManager | IsOwner]

class SubscriptionAPIView(generics.CreateAPIView):

    def perform_create(self, serializer):
        new_subscription = serializer.save()
        new_subscription.owner = self.request.user
        new_subscription.learn_course = serializer
        new_subscription.save()

    def post(self, *args, **kwargs):
        user =  self.request.user

        course_id = self.request.data.get("learn_course")
        course_item = get_object_or_404(LearnCourse, id=course_id)

        subs_item = Subscription.objects.filter(user=user, learn_course=course_id)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            new_subscription = Subscription(user=user, learn_course=course_item)
            new_subscription.save()
            message = 'подписка добавлена'
        # Возвращаем ответ в API
        return Response({"message": message})