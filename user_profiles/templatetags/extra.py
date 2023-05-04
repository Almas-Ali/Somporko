from user_profiles.models import Comment
from django import template

register = template.Library()


@register.filter(name='get_count')
def get_count(post_id):
    cm = Comment.objects.filter(post=post_id)
    total = cm.count()
    return total
