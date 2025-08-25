import json
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from .models import Todo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



# Create your views here.

def index(request):
    if(request.method == "GET"):
        return JsonResponse({"res":"Request Method was get"})
    else:
        return HttpResponse("Not a get")
    
@login_required
def add_todo(request):
    if request.user:
        if request.method == "POST":
            try:
                data = json.loads(request.body.decode("utf-8"))

                todo = Todo.objects.create(
                    id = data.get("id"),
                    title = data.get("title"),
                    notes = data.get("notes" , ""),
                    important=data.get("important", False),
                    due_by = data.get("due_by"),
                    user = request.user
                    )
                return JsonResponse({
                    "message":"Todo succesfully created!!",
                    "todo":{
                        "id":todo.id,
                        "title":todo.title,
                        "notes":todo.notes,
                        "important":todo.important,
                        "due_by":todo.due_by,
                        "created_at":todo.created_at,
                        "owener": todo.user
                    }
                }, status=201)

            except Exception as e:
                return JsonResponse({"error":str(e)}, status=400)
        else:
            return JsonResponse({"error":"invalid request method"}, status=405)
    else:
        return JsonResponse({
            "error":"Not Signed In"
        })    

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

########AUTH#################



class RegisterView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        if request.method == "POST":
            try:
                data = json.loads(request.body.decode("utf-8"))
                username = data.get("username")
                email = data.get("email")
                password = data.get('password')
                if not username or not password:
                    return Response({"error":"Missing fields"}, status=status.HTTP_400_BAD_REQUEST)
                if User.objects.filter(username=username).exists():
                    return Response({"error":"User with this username already exists"}, status=status.HTTP_400_BAD_REQUEST)
                user = User(username=username, email=email)
                user.set_password(password)
                user.save()
                return Response({"message":"User successfully created"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"Error":"Something went wrong in the registry process."})

    def get(self,request):
        return Response("Request method not allowed", status=status.HTTP_403_FORBIDDEN)
    

class LoginView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"Error":"Invalid Login data"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error":"Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        res = JsonResponse({
            "message":"Successfully logged in",

        },status=status.HTTP_200_OK)
        access = str(refresh.access_token)
        res.set_cookie(
            key='access',
            value=access,
            httponly=True,
            # secure=True, ##add this in production (HTTPS)
            samesite="Lax",
            max_age=300000
        )
        res.set_cookie(
            key='refresh',
            value=str(refresh),
            httponly=True,
            # secure=True, ##add this in production (HTTPS)
            samesite="Lax",
            max_age=(300000*100)
        )
        return res



class LogoutView(APIView):
    permission_classes=[AllowAny]
    @csrf_exempt
    def post(self,request):
        res = JsonResponse({"message":"Successfully logged out"}, status=status.HTTP_200_OK)
        refreshtoken = request.COOKIES.get("refresh")
        if refreshtoken:
            token = RefreshToken(refreshtoken)
            token.blacklist()

        res.delete_cookie("access")
        res.delete_cookie("refresh")

        return res



class UserView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        return Response({
            "username":request.user.username,
            "email":request.user.email
        }, status=status.HTTP_200_OK)