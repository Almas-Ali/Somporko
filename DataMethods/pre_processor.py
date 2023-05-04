from friendship.models import FriendshipManager
import time

def all_page_processors(request):
    if request.user.is_authenticated:
        all_r = FriendshipManager.requests(request, request.user)
    else:
        all_r = None
    website_name = 'Somporko'
    site_icon = '/static/img/somporko.PNG'
    Year = time.strftime('%Y')

    return {
        "all_r": all_r,
        "config": {
            "website_name": website_name,
            "site_icon": site_icon,
            "year": Year,
        }
    }
