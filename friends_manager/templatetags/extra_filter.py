from django import template
from django.contrib.auth.models import User
from user_profiles.models import ProfilePost

register = template.Library()


@register.filter(name='get_user_pic')
def get_user_pic(username):
    try:
        p = ProfilePost.objects.filter(
            sno=username, is_profile_img=True).order_by('-date').first().img.url
    except:
        p = None
    return p


@register.filter(name='get_user_img_by_id')
def get_user_img_by_id(id):
    user = User.objects.get(id=id)
    print(user)
    try:
        p = ProfilePost.objects.filter(
            sno=user, is_profile_img=True).order_by('-date').first().img.url
    except:
        p = None
    return p


@register.filter(name='get_user_full_name')
def get_user_full_name(id):
    user = User.objects.get(id=id)
    return user.get_full_name()


@register.filter(name='get_username_by_id')
def get_username_by_id(id):
    user = User.objects.get(id=id)
    return user.username
