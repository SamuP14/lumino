from django.conf import settings
from django.db import models
from django.urls import reverse


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='student_enrollments',
        on_delete=models.CASCADE,
    )
    subject = models.ForeignKey(
        'subjects.Subject',
        related_name='subject_enrollments',
        on_delete=models.CASCADE,
    )
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return f'Student: {self.student}, Enrolled At: {self.enrolled_at}'


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
        return reverse('subjects:subject-detail', kwargs={'subject_code': self.code})

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
