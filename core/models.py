from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        INSTRUCTOR = 'INSTRUCTOR', 'Instructor'
        STUDENT = 'STUDENT', 'Student'

    role = models.CharField(
        max_length=15,
        choices=Roles.choices,
        default=Roles.STUDENT
    )
    email = models.EmailField(unique=True)

    # Use email instead of username for authentication:
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    qualification = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    biography = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='instructors/', blank=True, null=True)


    def __str__(self):
        return f"Instructor: {self.user.get_full_name() or self.user.username}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    learning_progress = models.IntegerField(default=0)  # Percentage tracker:

    def __str__(self):
        return f"Student: {self.user.get_full_name() or self.user.username}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify (self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Course(models.Model):
    class CourseLevels(models.TextChoices):
        BEGINNER = 'BEGINNER', 'Beginner'
        INTERMEDIATE = 'INTERMEDIATE', 'Intermediate'
        ADVANCED = 'ADVANCED', 'Advanced'

    class CourseStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PUBLISHED = 'PUBLISHED', 'Published'
        ARCHIVED = 'ARCHIVED', 'Archived'

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='courses')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_courses')
    duration = models.IntegerField(help_text="Duration in hours")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    level = models.CharField(max_length=20, choices=CourseLevels.choices, default=CourseLevels.BEGINNER)
    status = models.CharField(max_length=20, choices=CourseStatus.choices, default=CourseStatus.DRAFT)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
