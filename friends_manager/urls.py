from django.urls import path, include
from friends_manager import views

urlpatterns = [

    # Friend settings urls

    path('list/id=<int:id>', views.friendlist, name='friendlist'),
    path('add-friend/id=<int:id>', views.add_friend, name='add-friend'),
    path('remove-friend-confirmation/id=<int:id>',
         views.remove_friend_confirmation, name='remove-friend-confirmation'),
    path('remove-friend/id=<int:id>', views.remove_friend, name='remove-friend'),
    path('sent-request', views.sent_request, name='sent-request'),
    path('cancel-friend/id=<int:id>', views.cancel_friend, name='cancel-friend'),
    path('friend-requests', views.friend_requests, name='friend-requests'),
    path('accept-request/id=<int:id>',
         views.accept_request, name='accept-request'),
    path('decline-request/id=<int:id>',
         views.decline_request, name='decline-request'),

    # Follower settings urls

    path('add-follow/id=<int:id>', views.add_follow, name='add-follow'),
    path('cancel-follow/id=<int:id>', views.cancel_follow, name='cancel-follow'),

]
