import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.middleware.csrf import get_token
from .models import Todo

# Create your views here.

def index(request):
    if(request.method == "GET"):
        return JsonResponse({"res":"Request Method was get"})
    else:
        return HttpResponse("Not a get")
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
            todos = Todo.objects.all().values("id","title", "important","due_by","created_at","notes", "completed")
            return JsonResponse(list(todos), safe=False, status=200)
        
        except Exception as e:
            return JsonResponse({"error":e}, status=400)
    else:
        return JsonResponse({"message":"Invalid Request Type"})
        
def getCompletedTodos(request):
    if request.method == 'GET':
        try:
            todos = Todo.objects.filter(completed=True).values("id","title", "important","due_by","created_at","notes", "completed")
            return JsonResponse(list(todos), safe=False, status=200)
        
        except Exception as e:
            return JsonResponse({"error":e}, status=400)
    else:
        return JsonResponse({"message":"Invalid Request Type"})


def editTodo(request,id):
    if request.method == 'PUT': 
        try:
            data = json.loads(request.body.decode("utf-8"))
            id = id
            todo = Todo.objects.get(id=id)
            todo.title = data.get('title', todo.title)
            todo.notes = data.get('notes', todo.notes)
            todo.important = data.get('important', todo.important)
            todo.due_by = data.get('due_by', todo.due_by)
            todo.completed = data.get('completed', todo.completed)
            todo.save()
            return JsonResponse({
                "message":"Todo succesffully updated",
                "todo":{
                    "id":todo.id,
                    "title":todo.title,
                    "notes":todo.notes,
                    "important":todo.important,
                    "due_by":todo.due_by,
                    "completed":todo.completed
                }
            }, status=200)
        except Todo.DoesNotExist:
            return JsonResponse({"error":"Todo does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"error":str(e)}, status=400)
    else:
        return JsonResponse({"message":"Invalid Request Type"},status=405)

def deleteTodo(request, id):
    if request.method=="DELETE":
        try:
            todo = Todo.objects.get(id = id)
            todo.delete()
            return JsonResponse({"message":"Record Successfully Deleted"}, status = 200)
        except Todo.DoesNotExist:
            return JsonResponse({"error":"Todo does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"message":e})
    else:
        return JsonResponse({"message":"Invalid request Type"})
    
def getTodo(request,id):
    if request.method=="GET":
        try:
            currTodo=Todo.objects.get(id=id)
            
            return JsonResponse({
                    "todo": {
                        "id": currTodo.id,
                        "title": currTodo.title,
                        "notes": currTodo.notes,
                        "important": currTodo.important,
                        "due_by": currTodo.due_by,
                        "completed": currTodo.completed,
                        "created_at": currTodo.created_at
                    }
                }, status=200)

        
        except Todo.DoesNotExist:
            return JsonResponse({"error":"Todo does not exist!"})

        except Exception as e:
            return JsonResponse({"error":e})


def getCSRF(request):
    return JsonResponse({
        "csrfToken":get_token(request)
    })





#         {
#     "message": "Todo succesfully created!!",
#     "todo": {
#         "id": "0000-0000-0000-0000-0000-1111",
#         "title": "Integrate Django With React", SAMPLE FOR HOW TODO SHOULD LOOK
#         "notes": "",
#         "important": "True",
#         "due_by": "2025-08-21",
#         "created_at": "2025-08-21"
#     }
# }