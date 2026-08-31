from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from weblearn.models import LearnCourse, Lesson
from users.models import User

class WebLearnTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="admin@example.com", )
        self.learn_course = LearnCourse.objects.create(title="Курс 1", description="Тестирование создания курса", owner=self.user)
        self.lesson = Lesson.objects.create(title="Тест", description="Тестирование создания урока", learn_course=self.learn_course
                                            , owner=self.user, video_link= 'http://youtube.com')
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """ Проверяет создание уроков """
        url = reverse('weblearn:lesson-create')
        data = {
            'title': 'Урок 1',
            'description': 'Тестирование создания урока',
            'learn_course': 1,
            'video_link': 'http://youtube.com'
        }

        response = self.client.post(
            url,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            data.get("title"), response.json().get("title")
        )
        self.assertEqual(
            data.get("description"), response.json().get("description")
        )

    def test_lesson_retrieve(self):

        url = reverse('weblearn:lesson-retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        obj = {
            'title': 'Тест',
            'description': 'Тестирование создания урока',
            'learn_course': self.learn_course,
            'video_link': 'http://youtube.com'
        }
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'),
            obj.get('title')
        )
        self.assertEqual(
            data.get('description'),
            obj.get('description')
        )
        self.assertEqual(
            data.get('learn_course'),
            obj.get('learn_course').id
        )
        self.assertEqual(
            data.get('video_link'),
            obj.get('video_link')
        )