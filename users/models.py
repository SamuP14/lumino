from django.conf import settings
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'S', 'Student'
        TEACHER = 'T', 'Teacher'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        max_length=1,
        choices=Role,
        default=Role.STUDENT,
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to='avatars',
        default='avatars/noavatar.png',
    )

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'user_username': self.user.username})

    def is_student(self):
        return self.role == self.Role.STUDENT

    def get_role(self):
        return self.get_role_display()

    def __str__(self):
        return f'User: {self.user}, Role: {self.role}'
