from rest_framework import serializers
from .models import User, Category, Course, StudentProfile, InstructorProfile, Lesson, Enrollment, Assignment, AssignmentSubmission, Quiz, QuizQuestion, QuizAttempt
from rest_framework.validators import UniqueTogetherValidator


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

    # FIXED: This line automatically passes the current user into validation!
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_email', 'course',
            'course_title', 'enrolled_at', 'is_completed'
        ]
        
        read_only_fields = ['is_completed']

        #def validate(self, data):
            # Extract the request from context safely
            #request = self.context.get('request')

            # Fallback check: If context is missing for any reason, use a safe check
           # if request and request.user:
               # user = request.user
               # if Enrollment.objects.filter(student=user, course=data['course']).exists():
                #    raise serializers.ValidationError("You are already enrolled in this course.")
               # return data

        # Django's native validator intercepts duplicates before it hits the DB level!
        validators = [
            UniqueTogetherValidator(
                queryset=Enrollment.objects.all(),
                fields=['student', 'course'],
                message="You are already enrolled in this course."
            )
        ]

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'course', 'title', 'description', 'due_date', 'max_marks', 'created_at']

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_email = serializers.CharField(source='student.email', read_only=True)
    # Automatically bind the current student context
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'student', 'student_email', 'submitted_file', 'submitted_at', 'marks_obtained', 'feedback', 'is_graded']
        read_only_fields = ['marks_obtained', 'feedback', 'is_graded']

        validators = [
            UniqueTogetherValidator(
                queryset=AssignmentSubmission.objects.all(),
                fields=['student', 'assignment'],
                message="You have already submitted an answer file for this assignment."
            )
        ]

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'course', 'title', 'max_attempts', 'pass_percentage', 'questions']

class QuizAttemptSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # The student will submit answers structured as an array of objects: [{"question_id": 1, "selected_option": "A"}]
    answers_submitted = serializers.JSONField(write_only=True)

    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'student', 'score', 'passed', 'answers_submitted', 'attempted_at']
        read_only_fields = ['score', 'passed', 'attempted_at']


    def validate(self, data):
        # Enforce maximum attempt boundary conditions
        request = self.context.get('request')
        quiz = data['quiz']
        attempt_count = QuizAttempt.objects.filter(student=request.user, quiz=quiz).count()
        if attempt_count >= quiz.max_attempts:
            raise serializers.ValidationError(f"You have reached the maximum allowed attempts ({quiz.max_attempts}) for this quiz.")
        return data

    def create(self, validated_data):
        quiz = validated_data['quiz']
        student = validated_data['student']
        answers = validated_data['answers_submitted'] # Array parsed directly from Postman

        total_questions = quiz.questions.count()
        if total_questions == 0:
            return QuizAttempt.objects.create(quiz=quiz, student=student, score=0.00, passed=False)

        correct_count = 0
        for entry in answers:
            try:
                question = quiz.questions.get(id=entry.get('question_id'))
                if question.correct_option == entry.get('selected_option'):
                    correct_count += 1
            except QuizQuestion.DoesNotExist:
                continue # Skip invalid question IDs safely

        # Calculate score percentage
        final_score = (correct_count / total_questions) * 100
        has_passed = final_score >= quiz.pass_percentage

        return QuizAttempt.objects.create(
            quiz=quiz,
            student=student,
            score=final_score,
            passed=has_passed
        )
