"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views import (
    RegisterView,
    CategoryListCreateView,
    CourseListCreateView,
    CourseDetailView,
    LessonListCreateView,
    LessonDetailView,
    EnrollmentListCreateView,
    AssignmentListCreateView,
    AssignmentSubmissionListCreateView,
    QuizListCreateView, QuizAttemptListCreateView,
    InstructorGradeSubmissionView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Configure the visual header info for your LMS Capstone Project API:
schema_view = get_schema_view(
    openapi.Info(
        title="LMS Portal Backend API",
        default_version='v1',
        description="Interactive documentation landscape detailing all available REST framework endpoints for Students, Instructors, and Admin roles.",
        terms_of_service="https://google.com",
        contact=openapi.Contact(email="admin@lms.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,), # Publicly accessible for submission reviewers!
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Swagger Interactive Docs Paths
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                

    # Auth Endpoints from PRD
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Second wave endpoints starts here: Categories & Courses
    path('api/categories/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('api/courses/', CourseListCreateView.as_view(), name='course_list_create'),
    path('api/courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),

    # Lessons:
    path('api/lessons/', LessonListCreateView.as_view(), name='lesson_list_create'),
    path('api/lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('api/enrollments/', EnrollmentListCreateView.as_view(), name='enrollment_list_create'),

    # Assignment Routes:
    path('api/assignments/', AssignmentListCreateView.as_view(), name='assignment_list_create'),
    path('api/submissions/', AssignmentSubmissionListCreateView.as_view(), name='submission_list_create'),

    # Quiz Routes:
    path('api/quizzes/', QuizListCreateView.as_view(), name='quiz_list_create'),
    path('api/quizzes/attempts/', QuizAttemptListCreateView.as_view(), name='quiz_attempt_list_create'),

    
    # Final Grading Route
    path('api/submissions/<int:pk>/grade/', InstructorGradeSubmissionView.as_view(), name='instructor_grade_submission'),
]
