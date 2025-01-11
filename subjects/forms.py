from crispy_bootstrap5.bootstrap5 import Field, FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Row, Submit
from django import forms

from .models import Enrollment, Lesson, Subject


class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = (
            'title',
            'content',
        )

    def __init__(self, subject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subject = subject
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.layout = Layout(
            FloatingField('title'),
            FloatingField('content'),
            Submit('submit', 'Submit', css_class='w-100 mt-2 mb-2'),
        )

    def save(self, *args, **kwargs):
        lesson = super().save(commit=False)
        lesson.subject = self.subject
        lesson = super().save(*args, **kwargs)
        return lesson


class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = (
            'title',
            'content',
        )
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'style': 'width: 100%; height: 300px;',
                    'class': 'form-control',
                    'placeholder': 'Escribe el contenido aquí...',
                }
            ),
        }

    def __init__(self, subject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subject = subject
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.layout = Layout(
            FloatingField('title'),
            FloatingField('content'),
            Submit('submit', 'Submit', css_class='w-100 mt-2 mb-2'),
        )


class EditMarkForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['mark']


class EditMarkFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_show_labels = False
        self.layout = Layout(
            Row(
                HTML(
                    '{% load subject_extras %} <div class="col-md-5">{% student_label formset forloop.counter0 %}</div>'
                ),
                Field('mark', wrapper_class='col-md-2'),
                css_class='align-items-baseline',
            )
        )
        self.add_input(Submit('save', 'Save marks', css_class='mt-3'))


class EnrollSubjectsForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Obtener el usuario actual desde la vista
        super().__init__(*args, **kwargs)

        # Filtrar las asignaturas que el estudiante ya está matriculado
        enrolled_subjects = Enrollment.objects.filter(student=user).values_list(
            'subject', flat=True
        )
        self.fields['subjects'].queryset = Subject.objects.exclude(id__in=enrolled_subjects)

    def save(self, user):
        # Guardar las inscripciones (enrollments) para el estudiante en las asignaturas seleccionadas
        subjects_to_enroll = self.cleaned_data['subjects']
        for subject in subjects_to_enroll:
            Enrollment.objects.create(student=user, subject=subject)


class UnenrollSubjectsForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Obtener el usuario actual desde la vista
        super().__init__(*args, **kwargs)

        # Filtrar las asignaturas de las que el estudiante está matriculado
        enrolled_subjects = Enrollment.objects.filter(student=user).values_list(
            'subject', flat=True
        )
        self.fields['subjects'].queryset = Subject.objects.filter(id__in=enrolled_subjects)

    def save(self, user):
        # Eliminar las inscripciones de las asignaturas seleccionadas
        subjects_to_unenroll = self.cleaned_data['subjects']
        Enrollment.objects.filter(student=user, subject__in=subjects_to_unenroll).delete()
