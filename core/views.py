from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Category, Lesson, Enrollment
from .serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from .models import Course, Assignment, AssignmentSubmission, Quiz, QuizAttempt
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer, AssignmentSerializer, AssignmentSubmissionSerializer, QuizSerializer, QuizAttemptSerializer
from .permissions import IsInstructor # <-- Custom Security Role Check:

class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RegisterView(APIView):
    # AllowAny ensures guests can hit this endpoint to create an account:
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseListCreateView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Configure the filter engines:
    filter_backends = [DjangoFilterBackend, SearchFilter]

    # Exact match filters (e.g. ?level=BEGINNER&category=1):
    filterset_fields = ['level', 'category', 'status']

    # Text search filters (e.g. ?search=Python):
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        # Dynamically injects the logged-in user as the course instructor:
        serializer.save(instructor=self.request.user)

class CourseDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LessonListCreateView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LessonDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EnrollmentListCreateView(ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    # Only authenticated users can enroll or view enrollments
    # Filter the queryset so students can ONLY see their own enrollments
    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the logged-in user as the enrolling student
        serializer.save(student=self.request.user)


    # Add this method to inject the user into the data BEFORE validation happens
    #def create(self, request, *args, **kwargs):
        #data = request.data.copy()
        # Force the student field to be the current authenticated user's ID
        #data['student'] = request.user.id
        #serializer = self.get_serializer(data=data)
        #serializer.is_valid(raise_exception=True)
        #self.perform_create(serializer)
        #headers = self.get_success_headers(serializer.data)
        #return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AssignmentListCreateView(ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AssignmentSubmissionListCreateView(ListCreateAPIView):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer

    # Filter submissions so students can only track their own file uploads
    def get_queryset(self):
        if self.request.user.role == 'INSTRUCTOR':
            return AssignmentSubmission.objects.all()
        return AssignmentSubmission.objects.filter(student=self.request.user)

class QuizListCreateView(ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class QuizAttemptListCreateView(ListCreateAPIView):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer

    def get_queryset(self):
        # Instructors see all score histories; students track only their own marks
        if self.request.user.role == 'INSTRUCTOR':
            return QuizAttempt.objects.all()
        return QuizAttempt.objects.filter(student=self.request.user)


class InstructorGradeSubmissionView(UpdateAPIView):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsInstructor]  # <-- Strictly locks down editing rights to teachers

    def perform_update(self, serializer):
        # Automatically mark the submission as processed and graded upon save
        serializer.save(is_graded=True)
