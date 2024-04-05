from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *


class TrainingEnrollmentForm(forms.ModelForm):
    class Meta:
        model = TrainingEnrollment
        fields = ["training", "student", "user"]


class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ["title", "course_category", "image", "description"]

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)


class CourseStepForm(forms.ModelForm):
    class Meta:
        model = CourseSteps
        fields = ["title", "description"]

    def __init__(self, *args, **kwargs):
        super(CourseStepForm, self).__init__(*args, **kwargs)


class CourseStepsVideosForm(forms.ModelForm):
    class Meta:
        model = CourseStepsVideos
        fields = ["video"]

    def __init__(self, *args, **kwargs):
        super(CourseStepsVideosForm, self).__init__(*args, **kwargs)


class TrainingsForm(forms.ModelForm):
    class Meta:
        model = Trainings
        fields = ["title", "training_category", "image", "description", "start_date", "end_date"]

        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-control'}),
        #     'training_category': forms.Select(attrs={'class': 'form-control'}),
        #     'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        #     'description': CKEditorUploadingWidget(attrs={'class': 'form-control'}),
        #     'start_date': forms.DateInput(attrs={'class': 'form-control'}),
        #     'end_date': forms.DateInput(attrs={'class': 'form-control'}),
        # }

    def __init__(self, *args, **kwargs):
        super(TrainingsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class JobsForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ["title", "job_category", "location", "application_link", "application_close", "image", "description"]

    def __init__(self, *args, **kwargs):
        super(JobsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
