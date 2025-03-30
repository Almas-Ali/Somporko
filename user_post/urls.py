from django.contrib import admin
from django.urls import path, include
from user_post import views

app_name = 'posts'

urlpatterns = [
    path('<str:username>/id=<int:id>', views.post, name='post'),
]