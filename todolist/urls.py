"""
URL configuration for todolist_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from .views import LogoutView, RegisterView, LoginView, UserView, AddTodoView, EditView, DeleteView, GetTodosView,getCompletedTodosView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path("api/post", AddTodoView.as_view(), name="add"),
    path("api/get",GetTodosView.as_view(), name="get_todos"),
    path("api/delete/<str:id>",DeleteView.as_view(), name='delete'),
    path("api/edit/<str:id>",EditView.as_view(), name='edit'),
    path("api/get/completed", getCompletedTodosView.as_view(), name="get_completed_todos"),
    path("api/get/<str:id>", EditView.as_view(), name='edit_get'),
    path("api/getCSRF", views.getCSRF),
    path("api/register", RegisterView.as_view(), name='register'),
    path('api/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("api/login/",LoginView.as_view(), name="login" ),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/user/",UserView.as_view(), name="user" )

]
