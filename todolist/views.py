import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Todo

# Create your views here.

def index(request):
    if(request.method == "GET"):
        return JsonResponse({"res":"Request Method was get"})
    else:
        return HttpResponse("Not a get")
@csrf_exempt 
def add_todo(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            todo = Todo.objects.create(
                id = data.get("id"),
                title = data.get("title"),
                notes = data.get("notes" , ""),
                important=data.get("important", False),
                due_by = data.get("due_by")
                )
            return JsonResponse({
                "message":"Todo succesfully created!!",
                "todo":{
                    "id":todo.id,
                    "title":todo.title,
                    "notes":todo.notes,
                    "important":todo.important,
                    "due_by":todo.due_by,
                    "created_at":todo.created_at
                }
            }, status=201)
        
        except Exception as e:
            return JsonResponse({"error":str(e)}, status=400)
    else:
        return JsonResponse({"error":"invalid request method"}, status=405)
        

def getTodos(request):
    if request.method == 'GET':
        try:
            todos = Todo.objects.all().values("id","title", "important","due_by","created_at","notes")
            return JsonResponse(list(todos), safe=False, status=200)
        
        except Exception as e:
            return JsonResponse({"error":e}, status=400)