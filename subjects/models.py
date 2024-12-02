from django.conf import settings
from django.db import models
from django.urls import reverse

from users.models import Enrollment


class Subject(models.Model):
    code = models.CharField(
        max_length=3,
        unique=True,
    )
    name = models.CharField(max_length=128)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='teacher_subjects',
        on_delete=models.CASCADE,
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='students_subjects',
        through=Enrollment,
    )

    def get_absolute_url(self):
        return reverse('subjects:subject-detail', kwargs={'code': self.code})

    def __str__(self):
        return self.code


class Lesson(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    subject = models.ForeignKey(
        'subjects.Subject',
        related_name='lessons',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Title: {self.title}, Subject: {self.subject}'
