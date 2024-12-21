from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from .models import Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio')
        widgets = {
            'bio': forms.Textarea(
                attrs={
                    'style': 'width: 100%; height: 300px;',
                    'class': 'form-control',
                    'placeholder': 'Enter your bio here...',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True, enctype='multipart/form-data')
        self.helper.layout = Layout(
            'avatar',
            FloatingField('bio'),
            Submit('submit', 'Save', css_class='w-100 mt-2 mb-2'),
        )
