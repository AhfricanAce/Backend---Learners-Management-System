from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, InstructorProfile, StudentProfile

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    # Columns that will show up in the Admin list view:
    list_display = ['email', 'username', 'role', 'is_staff', 'is_active']


    # Allows editing the role inside the user page:
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Role Selection', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Role Selection', {'fields': ('role')}),
    )

# Register our models so they show up on the web dashboard:
admin.site.register(User, CustomUserAdmin)
admin.site.register(InstructorProfile)
admin.site.register(StudentProfile)
