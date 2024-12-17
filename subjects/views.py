from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import AddLessonForm, EditLessonForm
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

    lessons = subject.lessons.all()

    return render(
        request,
        'subjects/subject_detail.html',
        dict(
            subject=subject,
            lessons=lessons,
        ),
    )


@login_required
def lesson_detail(request, subject_code, lesson_pk):
    subject = Subject.objects.get(code=subject_code)
    lesson = subject.lessons.get(pk=lesson_pk)

    return render(
        request,
        'lessons/lesson_detail.html',
        dict(
            subject=subject,
            lesson=lesson,
        ),
    )


@login_required
def add_lesson(request, subject_code):
    subject = Subject.objects.get(code=subject_code)
    if request.method == 'GET':
        form = AddLessonForm(subject)
    else:
        if (form := AddLessonForm(subject, data=request.POST)).is_valid():
            form.save()
            return redirect(subject)
    return render(request, 'lessons/add_lesson.html', dict(form=form))


@login_required
def edit_lesson(request, subject_code, lesson_pk):
    subject = Subject.objects.get(code=subject_code)
    lesson = subject.lessons.get(pk=lesson_pk)

    if request.method == 'GET':
        form = EditLessonForm(subject, instance=lesson)
    else:
        if (form := EditLessonForm(subject, data=request.POST, instance=lesson)).is_valid():
            form.save()
            return redirect(subject)
    return render(
        request, 'lessons/edit_lesson.html', dict(form=form, subject=subject, lesson=lesson)
    )


@login_required
def delete_lesson(request, subject_code, lesson_pk):
    subject = Subject.objects.get(code=subject_code)
    lesson = subject.lessons.get(pk=lesson_pk)

    lesson.delete()
    return redirect(subject)


@login_required
def mark_list(request, subject):
    pass


@login_required
def edit_marks(request):
    pass


@login_required
def enroll_subjects(request):
    pass


@login_required
def unenroll_subjects(request):
    pass
