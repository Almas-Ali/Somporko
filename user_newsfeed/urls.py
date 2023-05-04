from django.contrib import admin
from django.urls import path, include
from user_newsfeed import views

urlpatterns = [
    path('', views.newsfeed, name='newsfeed'),
    path('likepost/<str:post_id>', views.likepost, name='likepost'),
    path('commentpost/<str:post_id>', views.commentpost, name='commentpost'),
]
