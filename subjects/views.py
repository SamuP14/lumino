from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Subject


@login_required
def subject_list(request):
    if request.user.profile.is_student():
        subjects = request.user.students_subjects.all()
    else:
        subjects = request.user.teacher_subjects.all()

    return render(
        request,
        'subjects/subject_list.html',
        dict(subjects=subjects),
    )


@login_required
def subject_detail(request, subject_code):
    if request.user.profile.is_student():
        subject = request.user.students_subjects.get(code=subject_code)
    else:
        subject = request.user.teacher_subjects.get(code=subject_code)

    return render(
        request,
        'subjects/subject_detail.html',
        dict(subject=subject),
    )


@login_required
def subject_lessons(request, subject_code):
    # if request.user.profile.is_student():
    #     subjects = request.user.students_subjects.all()
    # else:
    #     subjects = request.user.teacher_subjects.all()
    subject = Subject.objects.get(code=subject_code)
    lessons = subject.lessons.all()
    return render(
        request,
        'lessons/lesson_list.html',
        {
            'subject': subject,
            'lessons': lessons,
        },
    )


@login_required
def lesson_detail(request):
    pass


@login_required
def add_lesson(request, subject):
    pass


@login_required
def edit_lesson(request):
    pass


@login_required
def delete_lesson(request):
    pass


@login_required
def mark_list(request, subject):
    pass


@login_required
def edit_marks(request):
    pass
