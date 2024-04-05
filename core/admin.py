from django.contrib import admin
import admin_thumbnails
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_display = [
        'title', 'slug', 'date'
    ]
    list_display_links = [
        'title', 'slug',
    ]
    ordering = ['-date']

@admin_thumbnails.thumbnail('video')
class CourseStepsVideosInline(admin.TabularInline):
    model = CourseStepsVideos
    extra = 1

@admin.register(CourseSteps)
class CoursesStepsAdmin(admin.ModelAdmin):
    inlines = [CourseStepsVideosInline]
    prepopulated_fields = {"slug": ["title"]}
    list_display = [
        'course', 'title', 'date'
    ]
    list_display_links = [
        'title',
    ]
    ordering = ['-date']

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_display = [
        'user', 'title', 'course_category', 'date'
    ]
    list_display_links = [
        'title',
    ]
    ordering = ['-date']

@admin.register(Trainings)
class TrainingsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_display = [
        'user', 'title', 'training_category', 'start_date', 'end_date', 'date'
    ]
    list_display_links = [
        'title',
    ]
    ordering = ['-date']

@admin.register(TrainingEnrollment)
class TrainingEnrollmentAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ["title"]}
    list_display = [
        'key', 'training', 'student', 'date',
    ]
    list_display_links = [
        'key',
    ]
    ordering = ['-date']

@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_display = [
        'user', 'title', 'job_category', 'application_close', 'date'
    ]
    list_display_links = [
        'title',
    ]
    ordering = ['-date']

@admin.register(JobsApplication)
class JobsApplicationAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ["title"]}
    list_display = [
        'key', 'job', 'student', 'date',
    ]
    list_display_links = [
        'key',
    ]
    ordering = ['-date']
