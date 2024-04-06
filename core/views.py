from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from .models import *
from .forms import *

@login_required(login_url='login')
def category_filter(request, slug):
    category = Category.objects.get(slug=slug)

    jobs = Jobs.objects.filter(job_category=category)
    courses = Courses.objects.filter(course_category=category)
    trainings = Trainings.objects.filter(training_category=category)

    context = {
        'category': category,
        'jobs': jobs,
        'courses': courses,
        'trainings': trainings,
    }

    template_name = 'core/categories_filter.html'
    return render(request, template_name, context)

@login_required(login_url='login')
def dashboard(request):
    user = request.user
    trainings = Trainings.objects.all()
    matching_training = Trainings.objects.filter(training_category=user.role).count()
    training_enrolled = TrainingEnrollment.objects.filter(student=user).count()
    jobs = Jobs.objects.all()
    matching_jobs = Jobs.objects.filter(job_category=user.role).count()
    job_applied = JobsApplication.objects.filter(student=user).count()

    categories = Category.objects.all().order_by('-date')

    context = {
        'trainings': trainings,
        'matching_training': matching_training,
        'jobs': jobs,
        'matching_jobs': matching_jobs,
        'training_enrolled': training_enrolled,
        'job_applied': job_applied,
        'categories': categories,
    }
    template_name = 'core/dashboard.html'
    return render(request, template_name, context)

@login_required(login_url='login')
def create_course(request):
    user = request.user
    if user.category not in ["Institute", "Trainer"]:
        messages.error(request, "You do not have permission to create a course.")
        return redirect('dashboard')  # Redirect to home or any other appropriate page

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.slug = slugify(course.title)  # Generate slug from title
            course.save()
            messages.success(request, 'Course created successfully.')
            return redirect('course_detail', course.slug)  # Redirect to home or any other relevant page
        else:
            messages.error(request, 'Failed to create course. Please check the form.')
    else:
        form = CourseForm()  # Create a new instance of the form

    context = {'form': form}
    template_name = 'core/create_course.html'
    return render(request, template_name, context)

@login_required
def add_course_step(request, slug):
    course = get_object_or_404(Courses, slug=slug)
    user = request.user

    # Check if the current user is the owner of the course
    if user != course.user:
        messages.error(request, "You do not have permission to add a course step.")
        return redirect('course_detail', slug=slug)

    if request.method == 'POST':
        form = CourseStepForm(request.POST)
        if form.is_valid():
            course_step = form.save(commit=False)
            course_step.course = course  # Link the course step to the course
            course_step.save()
            messages.success(request, 'Course step added successfully.')
            return redirect('course_detail', slug=slug)
        else:
            messages.error(request, 'Failed to add course step. Please check the form.')
    else:
        form = CourseStepForm()

    context = {
        'form': form,
        'course': course
    }
    return render(request, 'add_course_step.html', context)

@login_required(login_url='login')
def courses(request):
    courses = Courses.objects.all().order_by('-date')

    context = {
        'courses': courses,
    }
    template_name = 'core/courses.html'
    return render(request, template_name, context)

@login_required(login_url='login')
def course_detail(request, slug):
    course = Courses.objects.get(slug=slug)
    course_step = CourseSteps.objects.all().filter(course=course).order_by('date')
    course_step_videos = CourseStepsVideos.objects.all().order_by('id')

    # Check if the current user is the owner of the course
    # if request.user != course.user:
    #     messages.error(request, "You do not have permission to add a course step.")
    #     return redirect('course_detail', course.slug)  # Redirect to home or any other appropriate page

    if request.method == 'POST':
        form = CourseStepForm(request.POST)
        if form.is_valid():
            course_step_instance = form.save(commit=False)
            course_step_instance.course = course  # Link the course step to the course
            course_step_instance.save()
            messages.success(request, 'Course step added successfully.')
            return redirect('course_detail', slug=slug)
        else:
            messages.error(request, 'Failed to add course step. Please check the form.')
    else:
        form = CourseStepForm()

    context = {
        'course': course,
        'course_step': course_step,
        'course_step_videos': course_step_videos,
        'form': form,
    }
    template_name = 'core/course-detail.html'
    return render(request, template_name, context)

@login_required(login_url='login')
def add_course_step_video(request, course_step_id):
    course_step = get_object_or_404(CourseSteps, id=course_step_id)

    # Check if the current user is the owner of the course step's course
    if request.user != course_step.course.user:
        messages.error(request, "You do not have permission to add a video to this course step.")
        return redirect('dashboard')  # Redirect to home or any other appropriate page

    if request.method == 'POST':
        form = CourseStepsVideosForm(request.POST, request.FILES)
        if form.is_valid():
            course_step_video_instance = form.save(commit=False)
            course_step_video_instance.course_step = course_step
            course_step_video_instance.save()
            messages.success(request, 'Course step video added successfully.')
        else:
            messages.error(request, 'Failed to add course step video. Please check the form.')
    else:
        messages.error(request, 'Invalid request method.')

    # Redirect back to the course detail page
    return redirect('course_detail', slug=course_step.course.slug)

@login_required(login_url='login')
def create_training(request):
    user = request.user
    categories = Category.objects.all().order_by('-date')
    if user.category not in ["Institute", "Trainer"]:
        messages.error(request, "You do not have permission to create a Training.")
        return redirect('trainings')  # Redirect to home or any other appropriate page

    if request.method == 'POST':
        form = TrainingsForm(request.POST, request.FILES)
        if form.is_valid():
            training = form.save(commit=False)
            training.user = request.user
            training.slug = slugify(training.title)  # Generate slug from title
            training.save()
            messages.success(request, 'Training created successfully.')
            return redirect('trainings')  # Redirect to home or any other relevant page
        else:
            messages.error(request, 'Failed to create training. Please check the form.')
    else:
        form = TrainingsForm()  # Create a new instance of the form

    context = {
        'form': form,
        'categories': categories,
    }
    template_name = 'core/create_training.html'
    return render(request, template_name, context)


@login_required(login_url='login')
def trainings(request):
    trainings = Trainings.objects.all().order_by('-date')
    training_enrolled = TrainingEnrollment.objects.filter(student=request.user)
    context = {
        'trainings': trainings,
        'training_enrolled': training_enrolled,
    }
    template_name = 'core/trainings.html'
    return render(request, template_name, context)

from django.http import JsonResponse
@login_required(login_url='login')
def training_detail(request, slug):
    training = Trainings.objects.get(slug=slug)
    user = request.user

    try:
        training_enrolled = TrainingEnrollment.objects.get(training=training, student=user)
    except TrainingEnrollment.DoesNotExist:
        training_enrolled = None

    if user.is_authenticated and request.method == "POST":
        # Check if user is already enrolled
        if not TrainingEnrollment.objects.filter(training=training, student=user).exists():
            enrollment = TrainingEnrollment.objects.create(training=training, student=user)
            # Success message (optional)
            message = "You have successfully enrolled in the training!"
        else:
            # Already enrolled message
            message = "You are already enrolled in this training."
    else:
        # User not authenticated message
        message = "You need to be logged in to enroll."

    context = {
        'training': training,
        'training_enrolled': training_enrolled,
        'message': message
    }
    template_name = 'core/training-detail.html'
    return render(request, template_name, context)

@login_required(login_url='login')
def create_job(request):
    user = request.user
    categories = Category.objects.all().order_by('-date')
    if user.category not in ["Institute", "Trainer"]:
        messages.error(request, "You do not have permission to create a Job.")
        return redirect('jobs')  # Redirect to home or any other appropriate page

    if request.method == 'POST':
        form = JobsForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.slug = slugify(job.title)  # Generate slug from title
            job.save()
            messages.success(request, 'job created successfully.')
            return redirect('jobs')  # Redirect to home or any other relevant page
        else:
            messages.error(request, 'Failed to create jobs. Please check the form.')
    else:
        form = JobsForm()  # Create a new instance of the form

    context = {
        'form': form,
        'categories': categories,
    }
    template_name = 'core/create_job.html'
    return render(request, template_name, context)


@login_required(login_url='login')
def jobs(request):
    jobs = Jobs.objects.all().order_by('-date')

    # Retrieve the number of applicants for each job and add it to the job object
    for job in jobs:
        job.num_applicants = JobsApplication.objects.filter(job=job).count()

    context = {
        'jobs': jobs,
    }
    template_name = 'core/jobs.html'
    return render(request, template_name, context)

@login_required(login_url='login')
def job_detail(request, slug):
    job = Jobs.objects.get(slug=slug)
    user = request.user

    try:
        job_application = JobsApplication.objects.get(job=job, student=user)
    except JobsApplication.DoesNotExist:
        job_application = None

    if user.is_authenticated and request.method == "POST":
        # Check if user is already Applied
        if not JobsApplication.objects.filter(job=job, student=user).exists():
            application = JobsApplication.objects.create(job=job, student=user)
            # Success message (optional)
            message = "You have successfully Applied for this job"
        else:
            # Already enrolled message
            message = "You have already applied for this job"
    else:
        # User not authenticated message
        message = "You need to be logged in to Apply for the job."


    context = {
        'job': job,
        'job_application': job_application,
        'message': message,
        'num_applications': job.num_applications,
    }
    template_name = 'core/job-detail.html'
    return render(request, template_name, context)

@login_required(login_url='login')
def institutes(request):
    template_name = 'core/institutes.html'
    return render(request, template_name)

@login_required(login_url='login')
def institute_detail(request):
    template_name = 'core/institute-detail.html'
    return render(request, template_name)
