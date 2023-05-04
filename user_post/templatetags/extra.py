from django import template
from django.contrib.auth.models import User
from user_profiles.models import Comment, ProfilePost

register = template.Library()


@register.filter(name='get_count')
def get_count(post_id):
    cm = Comment.objects.filter(post=post_id)
    total = cm.count()
    return total


@register.filter(name='profile_picture_finder_user')
def profile_picture_finder_user(username):
    p = ProfilePost.objects.filter(
        sno=username, is_profile_img=True).order_by('-date').first()
    return p.img.url


@register.filter(name='get_full_name_user')
def get_full_name_user(username):
    try:
        p = User.objects.get(username=username).get_full_name()
    except:
        p = None
    return p


@register.filter(name='get_value')
def get_value(dict, value):
    return dict.get(value)
