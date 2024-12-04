from django.urls import path

from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('enroll/', views.enroll_subjects, name='enroll-subjects'),
    path('unenroll/', views.unenroll_subjects, name='unenroll-subjects'),
    path('<str:subject_code>/', views.subject_detail, name='subject-detail'),
    path('<str:subject_code>/lessons/', views.subject_lessons, name='subject-lessons'),
    path('<str:subject_code>/lessons/add/', views.add_lesson, name='add-lesson'),
    path('<str:subject_code>/lessons/<int:pk>/', views.lesson_detail, name='lesson-detail'),
    path('<str:subject_code>/lessons/<int:pk>/edit/', views.edit_lesson, name='edit-lesson'),
    path('<str:subject_code>/lessons/<int:pk>/delete/', views.delete_lesson, name='delete-lesson'),
    path('<str:subject_code>/lessons/marks/', views.mark_list, name='mark-list'),
    path('<str:subject_code>/lessons/marks/edit/', views.edit_marks, name='edit-marks'),
]
