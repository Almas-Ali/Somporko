from django import template
from user_profiles.models import ProfilePost

register = template.Library()


@register.filter(name='profile_picture_finder')
def profile_picture_finder(id):
    try:
        p = ProfilePost.objects.filter(
            sno=id, is_profile_img=True).order_by('-date').first().img.url
    except:
        p = None
    return p
