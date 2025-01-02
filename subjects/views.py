from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import AddLessonForm, EditLessonForm, EditMarkForm, EditMarkFormSetHelper
from .models import Enrollment, Subject


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
def subject_detail(request, subject_code: str):
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
def lesson_detail(request, subject_code: str, lesson_pk: int):
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
def add_lesson(request, subject_code: str):
    subject = Subject.objects.get(code=subject_code)
    if request.method == 'GET':
        form = AddLessonForm(subject)
    else:
        if (form := AddLessonForm(subject, data=request.POST)).is_valid():
            form.save()
            return redirect(subject)
    return render(request, 'lessons/add_lesson.html', dict(form=form))


@login_required
def edit_lesson(request, subject_code: str, lesson_pk: int):
    subject = Subject.objects.get(code=subject_code)
    lesson = subject.lessons.get(pk=lesson_pk)
    if request.method == 'GET':
        form = EditLessonForm(subject, instance=lesson)
    else:
        if (form := EditLessonForm(subject, data=request.POST, instance=lesson)).is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Changes were successfully saved.')
    return render(
        request,
        'lessons/edit_lesson.html',
        dict(form=form, subject=subject, lesson=lesson),
    )


@login_required
def delete_lesson(request, subject_code: str, lesson_pk: int):
    subject = Subject.objects.get(code=subject_code)
    lesson = subject.lessons.get(pk=lesson_pk)

    lesson.delete()
    messages.add_message(request, messages.INFO, 'Lesson was successfully deleted.')
    return redirect(subject)


@login_required
def mark_list(request, subject_code: str):
    subject = Subject.objects.get(code=subject_code)
    queryset = subject.enrollments.all()
    return render(
        request,
        'subjects/marks/mark_list.html',
        dict(subject=subject, enrollments=queryset),
    )


@login_required
def edit_marks(request, subject_code: str):
    subject = Subject.objects.get(code=subject_code)

    MarkFormSet = modelformset_factory(Enrollment, EditMarkForm, extra=0)
    queryset = subject.enrollments.all()
    if request.method == 'POST':
        if (formset := MarkFormSet(queryset=queryset, data=request.POST)).is_valid():
            formset.save()
            messages.add_message(request, messages.SUCCESS, 'Marks were successfully saved.')
            return redirect(reverse('subjects:edit-marks', kwargs={'subject_code': subject_code}))
    else:
        formset = MarkFormSet(queryset=queryset)
    helper = EditMarkFormSetHelper()
    return render(
        request,
        'subjects/marks/edit_marks.html',
        dict(subject=subject, formset=formset, helper=helper),
    )


@login_required
def enroll_subjects(request):
    pass


@login_required
def unenroll_subjects(request):
    pass
