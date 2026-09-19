from rest_framework import serializers
from .models import Category, Course

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']
        read_only_fields = ['slug'] # Handled automatically by the model save method

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
