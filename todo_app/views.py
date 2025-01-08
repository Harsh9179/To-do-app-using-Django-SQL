from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from datetime import datetime

# Home page with tasks
def home(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'todo_app/home.html', {'tasks': tasks})
    else:
        return redirect('login')

# Add Task
def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        priority = request.POST['priority']
        deadline = datetime.strptime(request.POST['deadline'], '%Y-%m-%dT%H:%M')
        Task.objects.create(title=title, description=description, priority=priority, deadline=deadline, user=request.user)
        return redirect('home')
    return render(request, 'todo_app/add_task.html')

# Edit Task
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.priority = request.POST['priority']
        task.deadline = datetime.strptime(request.POST['deadline'], '%Y-%m-%dT%H:%M')
        task.save()
        return redirect('home')
    return render(request, 'todo_app/edit_task.html', {'task': task})

# Delete Task
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    return render(request, 'todo_app/delete_task.html', {'task': task})

# User Signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'todo_app/signup.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'todo_app/login.html')

# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')
