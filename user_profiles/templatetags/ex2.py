from django import template
from django.contrib.auth.models import User
from django.http import request
from user_profiles.models import Comment, ProfilePost
from friendship.models import Friend, FriendshipManager
from django.core.files.images import get_image_dimensions

register = template.Library()


@register.filter(name='full_name')
def full_name(post_sno):
    u = User.objects.filter(username=post_sno).first().get_full_name()
    return u


@register.filter(name='picture_find')
def picture_find(post_id):
    # print(post_id)
    u = ProfilePost.objects.get(id=post_id)
    if u.img == '':
        u = None
    else:
        return u.img.url


# @register.filter(name='is_friend_reqested')
# def is_friend_reqested(from_id):
#     from_user = User.objects.get(id=from_id)
#     all_requests = Friend.objects.sent_requests(user=request.user)
#     print(all_requests)

#     return all_requests


@register.filter(name='get_image_height')
def get_image_height(post_id):
    post = ProfilePost.objects.get(id=post_id)

    width, height = get_image_dimensions(post.img)

    return height


@register.filter(name='get_image_width')
def get_image_width(post_id):
    post = ProfilePost.objects.get(id=post_id)

    width, height = get_image_dimensions(post.img)

    return width
