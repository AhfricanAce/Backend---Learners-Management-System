from rest_framework import serializers
from .models import User, Category, Course, StudentProfile, InstructorProfile, Lesson, Enrollment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'course',
            'title', 'description',
            'video_url', 'file_attachment',
            'order', 'created_at'
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']
        read_only_fields = ['slug'] # Handled automatically by the model save method


class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    # NESTED RELATIONSHIP: Desgined to pull all lessons connected to this course!:
    # 'lessons' matches the related_name we set in models.py
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title','description', 'category', 'category_name', 'instructor',
            'instructor_name', 'duration', 'price', 'level',
            'status', 'thumbnail', 'lessons', 'created_at'
        ]
        read_only_fields = ['instructor', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role']

    def create(self, validated_data):
        # Extracts role configuration, defaults to STUDENT is empty:
        role = validated_data.get('role', User.Roles.STUDENT)

        # Create user instance with securely encrypted password hashing:
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=role
        )

        # Automatically spin up the corresponding secondary profile wrapper:
        if user.role == User.Roles.INSTRUCTOR:
            InstructorProfile.objects.create(user=user)
        else:
            StudentProfile.objects.create(user=user)

        return user

class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_email', 'course',
            'course_title', 'enrolled_at', 'is_completed'
        ]
        read_only_fields = ['student', 'is_completed']

        def validate(self, data):
            # Extract the request from context safely
            request = self.context.get('request')

            # Fallback check: If context is missing for any reason, use a safe check
            if request and request.user:
                user = request.user
                if Enrollment.objects.filter(student=user, course=data['course']).exists():
                    raise serializers.ValidationError("You are already enrolled in this course.")
                return data
