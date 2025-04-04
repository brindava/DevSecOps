from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
from .views import LoginView, logout_view, quiz_home, SignUpView, create_question, create_choice, admin_dashboard

urlpatterns = [
    
    # Root URL (Login Page)
    path('', LoginView.as_view(), name='home'),
    
    # Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),

    # Admin (Teacher) Views
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('create-question/', create_question, name='create_question'),
    path('create-choice/<int:question_id>/', create_choice, name='create_choice'),
    path('edit-question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
    # Quiz (Student) Views
    path('quiz_home/', quiz_home, name='quiz_home'),
    path('quiz_page/', views.quiz_page, name='quiz_page'),  # Updated from take_quiz
    path('quiz_result/', views.quiz_result, name='quiz_result'),  # Updated from submit_quiz

    # Password Reset
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    # Forbidden Access
    path('403/', views.forbidden_view, name='forbidden'),
]