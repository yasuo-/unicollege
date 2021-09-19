from django import forms
from ..courses.models import Course
from ..users.models import ConnectBeautyVenue
from .models import StudentCompletedModule


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)


class PostCompletedForm(forms.ModelForm):
    class Meta:
        model = StudentCompletedModule
        fields = ('course', 'module',)


class ConnectBeautyVenueForm(forms.ModelForm):
    class Meta:
        model = ConnectBeautyVenue
        fields = ('email',)
