from django.contrib.auth.models import AbstractUser
from django.db import models

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
    #USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['username']

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
