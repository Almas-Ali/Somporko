from django.shortcuts import render, redirect
import time
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_profiles.models import ManageProfile, ProfilePost, Comment
from django.views.decorators.csrf import csrf_exempt
from user_newsfeed.models import Announcement
from friendship.models import FriendshipManager


theme = 'light'
text = 'dark'
navbar = 'primary'

theme, text = text, theme

@login_required(login_url='/login')
def newsfeed(request):
    if request.user.is_anonymous:
        return redirect('/login')

    announcement = Announcement.objects.all().order_by('-date')
    all_r = FriendshipManager.requests(request, request.user)

    hour = time.strftime('%H')
    hour = int(hour)

    if hour >= 1 and hour <= 3:
        greating = 'Good night. Hope your are doing well.'
    elif hour >= 4 and hour <= 11:
        greating = 'Good morning. Hope your are doing well.'
    elif hour >= 12 and hour <= 14:
        greating = 'Good afternoon. Hope your are doing well.'
    elif hour >= 15 and hour <= 23:
        greating = 'Good evening. Hope your are doing well.'
    else:
        greating = 'Hope your are doing well'

    user = User.objects.all()
    posts = ProfilePost.objects.all().order_by('-date')
    userInfo = ManageProfile.objects.all()
    userInfoPic = ProfilePost.objects.all().order_by('-date')

    context = {
        "greating": greating,
        "user": user,
        "userInfoPic": userInfoPic,
        "userInfo": userInfo,
        "posts": posts,
        "announcement": announcement[0],
        "all_r": all_r,
        "theme": theme,
        "text": text,
    }
    return render(request, 'news_feed/index.html', context)


@login_required(login_url='/login')
@csrf_exempt
def likepost(request, post_id):
    if request.method == 'GET':
        post_id = request.GET.get('post_id')
        post_obj = ProfilePost.objects.get(id=post_id)

        if request.user in post_obj.likes.all():
            post_obj.likes.remove(request.user)
        else:
            post_obj.likes.add(request.user)

    # like, created = Like.objects.get_or_create(
    #     user=request.user, post_id=post_id)

    # if not created:
    #     if like.value == 'Like':
    #         like.value = 'Unlike'
    #     else:
    #         like.value = 'Like'
    # like.save()

    return redirect(f'/newsfeed#{post_id}')


@login_required(login_url='/login')
@csrf_exempt
def commentpost(request, post_id):
    if request.method == 'GET':
        cmt = request.POST.get('comment')
        user = request.user
        post = request.POST.get('post_sno')
        cmtp = Comment(cmt=cmt, user=user, post=post)
        cmtp.save()

    return redirect(f'/newsfeed#{post_id}')
