from rest_framework import serializers
from .models import Category, Course

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']
        read_only_fields = ['slug'] # Handled automatically by the model save method
