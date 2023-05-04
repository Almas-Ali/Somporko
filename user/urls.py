from django.urls import path
from user import views

urlpatterns = [
    path('menu', views.user_menu, name='user_menu'),
    path('notifications', views.notifications, name='notifications'),
    path('comment', views.post_comment, name='comment'),
    path('reply', views.post_comment_reply, name='reply'),
]