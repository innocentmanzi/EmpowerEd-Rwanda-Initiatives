from django.utils import timezone
import uuid
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.models import *

JOB_LOCATION = (
    ('Remote', 'Remote'),
    ('Hybrid', 'Hybrid'),
    ('Onsite', 'Onsite'),
)

def can_create_course(user):
    """
        This function checks if a user has the permission to create a course based on their category.
    """
    if user.is_authenticated:
        return user.category in ["Trainer", "Institute"]  #    Replace with your category names
    else:
        return False


class Courses(models.Model):
    user = models.ForeignKey(User, related_name="created_course", on_delete=models.CASCADE, null=True, blank=True)
    course_category = models.ForeignKey(Category, related_name="course_category", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to='course/images/', null=True, blank=True)

    description = RichTextUploadingField(blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def create_course(self, user, course_data, course_steps_data, course_steps_videos_data):
        """
        This function creates a course and its associated steps and videos.
        Args:
            user: The user creating the course.
            course_data: A dictionary containing course details.
            course_steps_data: A list of dictionaries containing course step details.
            course_steps_videos_data: A list of dictionaries containing course step video details.
        Returns:
            The created course object or None if there are errors.
        """
        if not can_create_course(user):
            return None

        self.save(**course_data)

        course = Courses.objects.create(user=user, **course_data)
        for step_data in course_steps_data:
            course_step = CourseSteps.objects.create(course=course, **step_data)
            for video_data in course_steps_videos_data:
                if video_data['course_step'] == course_step.id:
                    CourseStepsVideos.objects.create(course_step=course_step, **video_data)
        return course

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

class CourseSteps(models.Model):
    course = models.ForeignKey(Courses, related_name="course_step", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255)

    description = RichTextUploadingField(blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Course Step'
        verbose_name_plural = 'Course Steps'

class CourseStepsVideos(models.Model):
    course_step = models.ForeignKey(CourseSteps, related_name="course_videos", on_delete=models.SET_NULL, null=True, blank=True)
    video = models.FileField(upload_to='course/videos/', null=True, blank=True)

    class Meta:
        verbose_name = 'Step Video'
        verbose_name_plural = 'Step Videos'

class Trainings(models.Model):
    user = models.ForeignKey(User, related_name="created_trainings", on_delete=models.CASCADE, null=True, blank=True)
    training_category = models.ForeignKey(Category, related_name="training_category", on_delete=models.SET_NULL, null=True, blank=True)
    # category = models.ForeignKey(Category, related_name="category_training", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    description = RichTextUploadingField(null=True, blank=True)
    image = models.ImageField(upload_to='training/images/', null=True, blank=True)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def duration(self):
        if self.start_date and self.end_date:
            duration = self.end_date - self.start_date
            if duration.days == 1:
                return str(duration.days) + " DAY"
            else:
                return str(duration.days) + " DAYS"
        else:
            return None

    class Meta:
        verbose_name = 'Training'
        verbose_name_plural = 'Trainings'

class  TrainingEnrollment(models.Model):
    training = models.ForeignKey(Trainings, related_name="training_enrolled", on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(User, related_name="enrolled", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4()
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        now = timezone.now()
        if self.training.end_date and (now > self.training.end_date or now < self.training.start_date):
            return True
        else:
            return False

    class Meta:
        verbose_name = 'Training enrolled'
        verbose_name_plural = 'Training enrolled'

class Jobs(models.Model):
    user = models.ForeignKey(User, related_name="created_jobs", on_delete=models.CASCADE, null=True, blank=True)
    job_category = models.ForeignKey(Category, related_name="job_category", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    location = models.CharField(max_length=255, choices=JOB_LOCATION, null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)
    image = models.ImageField(upload_to='job/images/', null=True, blank=True)

    application_close = models.DateTimeField(null=True, blank=True)
    application_link = models.URLField(null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def remaining_days(self):
        today = timezone.now().date()
        if self.application_close:
            remaining_time = self.application_close.date() - today
            if remaining_time.days < 0:
                return "Closed"
            else:
                if remaining_time.days <= 1:
                    return str(remaining_time.days) + " DAY LEFT"
                else:
                    return str(remaining_time.days) + " DAYS LEFT"
        else:
            return "Application close date not set"

    @property
    def num_applications(self):
        return self.job_applications.count()

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

class  JobsApplication(models.Model):
    job = models.ForeignKey(Jobs, related_name='job_applications', on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(User, related_name="jobs_applied", on_delete=models.CASCADE, null=True, blank=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.first_name + " applied for " + self.job.title

    class Meta:
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'

