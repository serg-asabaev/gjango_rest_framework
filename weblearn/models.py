from django.db import models

class LearnCourse(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    preview = models.ImageField(upload_to='learn_course/images', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['title',]


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='lesson/images', blank=True, null=True, verbose_name='Изображение')
    video_link = models.URLField(max_length=200)

    learn_course = models.ForeignKey(LearnCourse, blank=True, null=True, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['title',]