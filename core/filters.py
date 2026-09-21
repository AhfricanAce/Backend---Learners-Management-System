from django_filters import rest_framework as filters
from .models import Course

class CourseFilter(filters.FilterSet):
    # Allow filtering by a maximum price ceiling (e.g., ?price_max=50)
    price_max = filters.NumberFilter(field_name="price", lookup_expr='lte')

    # Allow filtering by a minimum price floor (e.g., ?price_min=10)
    price_min = filters.NumberFilter(field_name="price", lookup_expr='gte')

    # Text-based partial matches for title and description
    title = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ['level', 'category', 'status', 'price_max', 'price_min', 'title']
