from django import template
from django.contrib.auth.models import User
from user_profiles.models import Comment, ProfilePost
from django.core.files.images import get_image_dimensions

register = template.Library()


@register.filter(name='get_count')
def get_count(post_id):
    cm = Comment.objects.filter(post=post_id)
    total = cm.count()
    return total


@register.filter(name='profile_picture_finder')
def profile_picture_finder(username):
    try:
        p = ProfilePost.objects.filter(
            sno=username, is_profile_img=True).order_by('-date').first().img.url
    except:
        p = None
    return p


@register.filter(name='get_full_name_user')
def get_full_name_user(username):
    try:
        p = User.objects.get(username=username).get_full_name()
    except:
        p = None
    return p


@register.filter(name='picture_find')
def picture_find(post_id):
    # print(post_id)
    u = ProfilePost.objects.get(id=post_id)
    if u.img == '':
        u = None
    else:
        return u.img.url


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
