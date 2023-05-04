from django.contrib import admin
from django.urls import path, include
from user_post import views

urlpatterns = [
    path('<str:username>/id=<int:id>', views.post, name='post'),
]