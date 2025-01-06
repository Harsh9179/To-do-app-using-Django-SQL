# todo_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # This includes login, logout, password reset URLs
    path('', include('todo_app.urls')),  # Include our app's URLs
]
