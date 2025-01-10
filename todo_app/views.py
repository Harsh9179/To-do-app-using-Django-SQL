from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Task
from .forms import TaskForm

# Home page view
@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user)

    # Sorting logic
    sort_by = request.GET.get("sort_by", "deadline")
    if sort_by == "priority":
        tasks = tasks.order_by("priority")
    elif sort_by == "deadline":
        tasks = tasks.order_by("deadline")
    elif sort_by == "created_at":
        tasks = tasks.order_by("created_at")

    # Filtering logic
    filter_by = request.GET.get("filter_by", "all")
    if filter_by == "high_priority":
        tasks = tasks.filter(priority="High")
    elif filter_by == "overdue":
        tasks = tasks.filter(deadline__lt=now())
    elif filter_by == "completed":
        tasks = tasks.filter(completed=True)
    elif filter_by == "pending":
        tasks = tasks.filter(completed=False)

    context = {
        "tasks": tasks,
        "sort_by": sort_by,
        "filter_by": filter_by,
    }
    return render(request, "todo_app/home.html", context)

# Add a new task
@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added successfully!")
            return redirect("home")
        else:
            messages.error(request, "Error adding task. Please try again.")
    else:
        form = TaskForm()
    return render(request, "todo_app/add_task.html", {"form": form})

# Edit an existing task
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect("home")
        else:
            messages.error(request, "Error updating task. Please try again.")
    else:
        form = TaskForm(instance=task)
    return render(request, "todo_app/edit_task.html", {"form": form})

# Delete a task
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect("home")
    return render(request, "todo_app/delete_task.html", {"task": task})

# User Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "todo_app/login.html", {"form": form})

# User Logout
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")

# User Signup
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Account created successfully!")
                return redirect("home")
            else:
                messages.error(request, "Failed to sign up. Please try again.")
        else:
            messages.error(request, "Invalid details. Please check the form.")
    else:
        form = UserCreationForm()
    return render(request, "todo_app/signup.html", {"form": form})
