from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    path('dashboard/category/<slug:slug>/', views.category_filter, name='category_filter'),

    path('dashboard/create-course/', views.create_course, name='create_course'),
    path('dashboard/create-course/<int:course_step_id>/', views.add_course_step_video, name='add_course_step_video'),
    path('dashboard/courses', views.courses, name='courses'),
    path('dashboard/course/<slug:slug>/', views.course_detail, name='course_detail'),

    path('dashboard/create-training/', views.create_training, name='create_training'),
    path('dashboard/trainings', views.trainings, name='trainings'),
    path('dashboard/training/<slug:slug>/', views.training_detail, name='training_detail'),

    path('dashboard/create-job/', views.create_job, name='create_job'),
    path('dashboard/jobs', views.jobs, name='jobs'),
    path('dashboard/job/<slug:slug>/', views.job_detail, name='job_detail'),

    path('dashboard/institutes', views.institutes, name='institutes'),
    path('dashboard/institute/institute_detail/', views.institute_detail, name='institute_detail'),
]