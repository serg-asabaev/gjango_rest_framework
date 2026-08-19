from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from weblearn.apps import WeblearnConfig
from config.settings import MEDIA_ROOT
from weblearn.views import LearnCourseViewSet

app_name = WeblearnConfig.name

router = DefaultRouter()
router.register(r'learn_course', LearnCourseViewSet, basename = 'learn_courses')


urlpatterns = [

] + router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=MEDIA_ROOT)