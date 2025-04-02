from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View
from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory

class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz_home')
        return render(request, 'signup.html', {'form': form})
    

# Admin Dashboard for Teachers
@login_required
def admin_dashboard(request):
    if request.user.user_type != 'teacher':
        return render(request, '403.html')  # Forbidden for non-teachers

    questions = Question.objects.all()
    return render(request, 'quiz/admin_dashboard.html', {'questions': questions})


# Create Question (Teachers Only)
@login_required
def create_question(request):
    if request.user.user_type != 'teacher':
        return render(request, '403.html')  # Only teachers can create questions

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save()
            for i in range(4):  # Assuming 4 choices
                choice_text = request.POST.get(f'choice_text_{i}')
                is_correct = request.POST.get(f'is_correct_{i}') == 'on'
                if choice_text:
                    Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)
            return redirect('quiz_home')  # Redirect to quiz_home after saving
    else:
        question_form = QuestionForm()

    return render(request, 'quiz/create_question.html', {'form': question_form})
    


# Create Choice (Teachers Only)
@login_required
def create_choice(request, question_id):
    if request.user.user_type != 'teacher':
        return render(request, '403.html')  # Forbidden for non-teachers

    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('admin_dashboard')
    else:
        form = ChoiceForm()

    return render(request, 'quiz/create_choice.html', {'form': form, 'question': question})


# Take Quiz (Students Only)
@login_required
def quiz_page(request):
    questions = Question.objects.all()
    return render(request, 'quiz_page.html', {'questions': questions, 'user_type': request.user.user_type})
    


# Submit Quiz (Students Only)
@login_required
def quiz_result(request):
    if request.method == "POST":
        score = 0
        total_questions = Question.objects.count()
        for question in Question.objects.all():
            selected_choice_id = request.POST.get(f"question_{question.id}")
            if selected_choice_id:
                try:
                    selected_choice = Choice.objects.get(id=selected_choice_id)
                    if selected_choice.is_correct:
                        score += 1
                except Choice.DoesNotExist:
                    pass
        return render(request, 'quiz_result.html', {'score': score, 'total_questions': total_questions})

    return redirect('quiz_home')


# Quiz Home
@login_required
def quiz_home(request):
    return render(request, 'quiz_home.html') 


# Login View
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('quiz_home')
        return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

def forbidden_view(request):
    return render(request, '403.html')

@login_required
def edit_question(request, question_id):
    if request.user.user_type != 'teacher':
        return render(request, '403.html')  # Only teachers can edit questions

    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('quiz_page')  # Redirect to quiz page after editing
    else:
        form = QuestionForm(instance=question)

    return render(request, 'quiz/edit_question.html', {'form': form})

@login_required
def delete_question(request, question_id):
    if request.user.user_type != 'teacher':
        return render(request, '403.html')  # Only teachers can delete questions

    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.delete()
        return redirect('quiz_page')  # Redirect to quiz page after deleting

    return render(request, 'quiz/delete_question.html', {'question': question})