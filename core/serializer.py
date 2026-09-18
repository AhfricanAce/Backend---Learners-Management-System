from .models import Category, Course

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'descriptive']
        read_only_fields = ['slug'] # Handled automatically by the model save method
