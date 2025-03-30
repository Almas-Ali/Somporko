from django.urls import path
from user_messages import views

app_name = 'messages'

urlpatterns = [
    path('', views.message, name='messages'),
    path('user/id=<int:id>', views.chat_box, name='chat_box'),
    # path('user/id=<int:id>/send', views.msg_send, name='msg_send'),
]
