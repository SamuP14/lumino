from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse

from .decorators import student_required, teacher_required
from .forms import (
    AddLessonForm,
    EditLessonForm,
    EditMarkForm,
    EditMarkFormSetHelper,
    EnrollSubjectsForm,
    UnenrollSubjectsForm,
)
from .models import Enrollment, Subject


@login_required
def subject_list(request):
    return render(
        request,
        'subjects/subject_list.html',
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


@teacher_required
@login_required
def add_lesson(request, subject_code: str):
    subject = Subject.objects.get(code=subject_code)
    if request.method == 'GET':
        form = AddLessonForm(subject)
    else:
        if (form := AddLessonForm(subject, data=request.POST)).is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Lesson was successfully added.')
            return redirect(subject)
    return render(request, 'lessons/add_lesson.html', dict(form=form))


@teacher_required
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


@teacher_required
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


@student_required
@login_required
def enroll_subjects(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'S':
        return HttpResponseForbidden(
            'You are not allowed to enroll in subjects.'
        )  # Solo para alumnos

    # Si es un POST, procesamos el formulario
    if request.method == 'POST':
        form = EnrollSubjectsForm(
            request.POST, user=request.user
        )  # Pasamos el usuario actual al formulario
        if form.is_valid():
            form.save(user=request.user)  # Guardamos las inscripciones
            messages.success(
                request, 'Successfully enrolled in the chosen subjects.'
            )  # Mensaje de éxito
            return redirect('subjects:subject-list')  # Redirigir a la lista de asignaturas

    else:
        # Si es un GET, creamos el formulario vacío
        form = EnrollSubjectsForm(user=request.user)

    # Renderizamos el formulario
    return render(
        request,
        'subjects/enroll_subjects.html',
        {'form': form},
    )


@student_required
@login_required
def unenroll_subjects(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'S':
        return HttpResponseForbidden(
            'You are not allowed to unenroll from subjects.'
        )  # Solo para alumnos

    # Si es un POST, procesamos el formulario
    if request.method == 'POST':
        form = UnenrollSubjectsForm(
            request.POST, user=request.user
        )  # Pasamos el usuario actual al formulario
        if form.is_valid():
            form.save(user=request.user)  # Guardamos las desmatriculaciones
            messages.success(
                request, 'Successfully unenrolled from the chosen subjects.'
            )  # Mensaje de éxito
            return redirect('subjects:subject-list')  # Redirigir a la lista de asignaturas

    else:
        # Si es un GET, creamos el formulario vacío
        form = UnenrollSubjectsForm(user=request.user)

    # Renderizamos el formulario
    return render(
        request,
        'subjects/unenroll_subjects.html',
        {'form': form},
    )
