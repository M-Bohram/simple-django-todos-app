from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_or_list_todos, name='create_or_list_todos'),  # Create Todo
    path('<int:todo_id>/', views.read_or_update_or_delete_todos, name='read_or_update_or_delete_todos'),  # Update Todo
]