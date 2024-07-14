from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Todo
import json
# Create your views here.
@csrf_exempt
@require_http_methods(["GET", "POST"])
def create_or_list_todos(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            todo_item = data.get('item')
            if todo_item:
                todo = Todo.objects.create(item=todo_item)
                return JsonResponse({'message': 'Todo created successfully', 'item': todo.item, 'id': todo.id}, status=201)
            else:
                return JsonResponse({'error': 'Item field is required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    elif request.method == 'GET':
        todos = Todo.objects.all().values()
        return JsonResponse(list(todos), safe=False)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def read_or_update_or_delete_todos(request, todo_id):
    if request.method == 'GET':
        todo = Todo.objects.filter(id=todo_id).values().first()
        if todo:
            return JsonResponse(todo, safe=False)
        else:
            return JsonResponse({'error': 'Todo not found'}, status=404)
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            todo_item = data.get('item')
            completed = data.get('completed')

            todo = Todo.objects.filter(id=todo_id).first()
            if todo:
                if todo_item is not None:
                    todo.item = todo_item
                if completed is not None:
                    todo.completed = completed
                todo.save()
                return JsonResponse({'message': 'Todo updated successfully', 'item': todo.item, 'completed': todo.completed}, status=200)
            else:
                return JsonResponse({'error': 'Todo not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    elif request.method == "DELETE":
        todo = Todo.objects.filter(id=todo_id).first()
        if todo:
            todo.delete()
            return JsonResponse({'message': 'Todo deleted successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Todo not found'}, status=404)