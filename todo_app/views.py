from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Task

# Home page view
@login_required
def home(request):
    # Get all tasks for the logged-in user
    tasks = Task.objects.filter(user=request.user)

    # Sorting logic
    sort_by = request.GET.get("sort_by", "deadline")  # Default to sorting by deadline
    if sort_by == "priority":
        tasks = tasks.order_by("priority")  # Assuming 'priority' is an integer for sorting
    elif sort_by == "deadline":
        tasks = tasks.order_by("deadline")

    # Filtering logic
    filter_by = request.GET.get("filter_by", None)
    if filter_by == "high_priority":
        tasks = tasks.filter(priority="High")
    elif filter_by == "overdue":
        tasks = tasks.filter(deadline__lt=now())  # Filter overdue tasks

    context = {
        "tasks": tasks,
        "sort_by": sort_by,
        "filter_by": filter_by,
    }
    return render(request, "todo_app/home.html", context)

# Task List view (if needed, as a separate page for all tasks)
@login_required
def task_list(request):
    # Get all tasks for the logged-in user
    tasks = Task.objects.filter(user=request.user)

    # Sorting logic
    sort_by = request.GET.get("sort_by", "deadline")  # Default to sorting by deadline
    if sort_by == "priority":
        tasks = tasks.order_by("priority")  # Assuming 'priority' is an integer for sorting
    elif sort_by == "deadline":
        tasks = tasks.order_by("deadline")

    # Filtering logic
    filter_by = request.GET.get("filter_by", None)
    if filter_by == "high_priority":
        tasks = tasks.filter(priority="High")
    elif filter_by == "overdue":
        tasks = tasks.filter(deadline__lt=now())  # Filter overdue tasks

    context = {
        "tasks": tasks,
        "sort_by": sort_by,
        "filter_by": filter_by,
    }
    return render(request, "todo_app/task_list.html", context)

# Add a new task
@login_required
def add_task(request):
    # Handle adding a new task here
    # If the request is POST, save the task, else render a form for adding a task
    pass

# Edit an existing task
@login_required
def edit_task(request, task_id):
    # Handle editing a task here
    # Fetch the task by ID, then update its details based on the form submission
    pass

# Delete a task
@login_required
def delete_task(request, task_id):
    # Handle deleting a task here
    # Fetch the task by ID, then delete it
    pass

# User Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate and log in the user
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")  # Redirect to the home page after login
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
    return redirect("login")  # Redirect to login page after logout

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
                return redirect("home")  # Redirect to the home page after signup
            else:
                messages.error(request, "Failed to sign up. Please try again.")
    else:
        form = UserCreationForm()

    return render(request, "todo_app/signup.html", {"form": form})
