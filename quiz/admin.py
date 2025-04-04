"""
Admin module for the quiz app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Question, Choice

# Custom admin for CustomUser
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('User Type', {'fields': ('user_type',)}),
    )

# Custom admin for Question
class QuestionAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return request.user.user_type == 'teacher'

    def has_delete_permission(self, request, obj=None):
        return request.user.user_type == 'teacher'

    def has_add_permission(self, request):
        return request.user.user_type == 'teacher'

# Register models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)