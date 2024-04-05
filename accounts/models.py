from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from ckeditor_uploader.fields import RichTextUploadingField
from .manager import MyUserManager

GENDERS = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

ACCOUNT_TYPE = (
    ('Student', 'Student'),
    ('Trainer', 'Trainer'),
    ('Institute', 'Institute'),
)

JOB_LOCATION = (
    ('Remote', 'Remote'),
    ('Hybrid', 'Hybrid'),
    ('Onsite', 'Onsite'),
)

class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    description = RichTextUploadingField(blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def num_courses(self):
        return self.course_category.count()

    @property
    def num_Trainings(self):
        return self.training_category.count()

    @property
    def num_jobs(self):
        return self.job_category.count()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=250, unique=True, null=False, blank=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to="images/user_profile/", null=True, blank=True)

    category = models.CharField(choices=ACCOUNT_TYPE, max_length=100, default="Student", blank=True, null=True)
    gender = models.CharField(choices=GENDERS, max_length=100, blank=True, null=True)
    role = models.ForeignKey(Category, related_name="user_role", on_delete=models.SET_NULL, null=True, blank=True)

    verified = models.BooleanField(default=False)

    # required
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone']

    objects = MyUserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def num_courses(self):
        return self.created_course.count()

    @property
    def num_trainings(self):
        return self.created_trainings.count()

    @property
    def num_trainings_enrolled(self):
        return self.enrolled.count()

    @property
    def num_jobs(self):
        return self.created_jobs.count()

    @property
    def num_jobs_applied(self):
        return self.jobs_applied.count()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superadmin

    def has_module_perms(self, add_label):
        return True

