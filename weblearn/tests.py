from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from weblearn.models import LearnCourse, Lesson, Subscription
from users.models import User

class WebLearnTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="admin@example.com", )
        self.learn_course = LearnCourse.objects.create(title="Курс 1", description="Тестирование создания курса", owner=self.user)
        self.lesson = Lesson.objects.create(title="Тест", description="Тестирование создания урока", learn_course=self.learn_course
                                            , owner=self.user, video_link= 'http://youtube.com', )

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
        """ Проверяет просмотр уроков """
        url = reverse('weblearn:lesson-retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        obj = {
            'title': 'Тест',
            'description': 'Тестирование создания урока',
            'learn_course': self.learn_course,
            'video_link': 'http://youtube.com',
            'owner': self.user
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

    def test_lesson_update(self):
        """ Проверяет обновление уроков """
        url = reverse('weblearn:lesson-update', args=(self.lesson.pk,))
        data = {
            'title': 'Урок 2',
            'description': 'Тестирование создания урока',
            'learn_course': self.learn_course.pk,
            'video_link': 'http://youtube.com',
            'owner': self.user.id
        }
        response = self.client.patch(url, data)
        updated_data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            updated_data.get('title'),
            data.get('title')
        )

    def test_lesson_delete(self):
        """ Проверяет удаление уроков """
        url = reverse('weblearn:lesson-delete', args=(self.lesson.id,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            0
        )

    def test_lesson_list(self):
        """ Проверяет вывод списка уроков """
        url = reverse('weblearn:lesson-list')
        response = self.client.get(url)
        resp_data = response.json()

        data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.id,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "learn_course": self.learn_course.id,
                    "video_link": self.lesson.video_link,
                    "owner": self.user.pk
                },
            ]
        }
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            resp_data,
            data
        )

    def test_subscription(self):
        """ Проверяет подписку на курсы """
        url = reverse('weblearn:subscription-create')

        data = {
            "learn_course": self.learn_course.id
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json().get('message'),
            'подписка добавлена'
        )

        response = self.client.post(url, data)
        self.assertEqual(
            response.json().get('message'),
            'подписка удалена'
        )