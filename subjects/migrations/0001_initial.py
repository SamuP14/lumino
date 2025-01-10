# Generated by Django 5.1.4 on 2025-01-10 16:58

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_at', models.DateField(auto_now_add=True)),
                ('mark', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['student__last_name', 'student__first_name'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('students', models.ManyToManyField(related_name='students_subjects', through='subjects.Enrollment', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teacher_subjects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('content', models.TextField(blank=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='subjects.subject')),
            ],
        ),
        migrations.AddField(
            model_name='enrollment',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='subjects.subject'),
        ),
    ]
