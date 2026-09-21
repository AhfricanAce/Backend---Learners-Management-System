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
from django.urls import path
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
    AssignmentSubmissionListCreateView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

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
]
