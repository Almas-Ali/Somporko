from django import template
from django.contrib.auth.models import User
from django.http import request
from user_profiles.models import Comment, ProfilePost
from friendship.models import Friend, FriendshipManager

register = template.Library()


@register.filter(name='full_name')
def full_name(post_sno):
    u = User.objects.filter(username=post_sno).first().get_full_name()
    return u


# @register.filter(name='picture_find')
# def picture_find(post):
#     print(post)
#     try:
#         u = ProfilePost.objects.get(img=post)
#     except:
#         try:
#             u = ProfileImageUser.objects.get(img=post)
#         except:
#             u = None
#     return u


@register.filter(name='is_friend_reqested')
def is_friend_reqested(from_id):
    from_user = User.objects.get(id=from_id)
    all_requests = Friend.objects.sent_requests(user=request.user)
    print(all_requests)

    return all_requests
