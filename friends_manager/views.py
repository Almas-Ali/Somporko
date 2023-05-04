from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block, FriendshipRequest, FriendshipManager, FollowingManager
from user_profiles.models import ManageProfile, ProfilePost
from user_settings.models import UserPrivacy



theme = 'light'
text = 'dark'
navbar = 'primary'
theme, text = text, theme

context = {
    "theme": theme,
    "text": text,
}

def r_notice(request):
    all_r = FriendshipManager.requests(request, request.user)
    return all_r


@login_required(login_url='/login')
def friendlist(request, id):
    i = User.objects.get(id=id)
    friendlist0 = Friend.objects.friends(i)
    all_f = Friend.objects.filter(to_user=request.user)
    all_r = FriendshipManager.requests(request, request.user)
    # print(all_f[0].created)

    user = User.objects.get(id=id)
    userInfoPic = ProfilePost.objects.filter(sno=user, is_profile_img=True).order_by('-date').first()
    userInfoPicFriends = ProfilePost.objects.all().order_by('-date')

    if user == None:
        return HttpResponse('404 - Not found !')

    userInfo = ManageProfile.objects.filter(sno=user).first()
    userInfoFriends = ManageProfile.objects.all()
    hide_friends = UserPrivacy.objects.get(user=user).hide_friends

    
    try:
        is_friend = Friend.objects.are_friends(request.user, user)
    except:
        is_friend = False

    try:
        is_following = FollowingManager.follows(request, request.user, user)
    except:
        is_following = False

    try:
        is_sent_request = Friend.objects.can_request_send(request.user, user)
    except:
        is_sent_request = False

    try:
        total_follow = FollowingManager.followers(request, user)
    except:
        pass
    
    if all_r == []:
        requested_user = None
    else:
        for users in all_r:
            if users in all_r:
                requested_user = users
            else:
                requested_user = None

    context = {
        "userInfo": userInfo,
        "user": user,
        "userInfoPic": userInfoPic,
        "all_r": r_notice(request),
        "friendlist0": friendlist0,
        "userInfoPicFriends": userInfoPicFriends,
        "userInfoFriends": userInfoFriends,
        "all_f": all_f,
        "empty": [],
        "hide_friends": hide_friends,
        "is_friend": is_friend,
        "is_following": is_following,
        "is_sent_request": is_sent_request,
        "total_follow": total_follow,
        "requested_user": requested_user,
        "theme": theme,
        "text": text,
    }
    return render(request, 'friends_manager/friendlist.html', context)


@login_required(login_url='/login')
def add_friend(request, id):
    if request.method == 'POST':
        try:
            other_user = User.objects.get(id=id)
            Friend.objects.add_friend(request.user, other_user)
        except:
            pass
        path = request.POST.get('path')

    return redirect(path)


@login_required(login_url='/login')
def sent_request(request):
    s = Friend.objects.sent_requests(user=request.user)
    return HttpResponse('Total : ', s)


@login_required(login_url='/login')
def cancel_friend(request, id):
    if request.method == 'POST':
        other_user = User.objects.get(id=id)
        try:
            fr = FriendshipRequest.objects.get(to_user=other_user)
            fr.cancel()
        except:
            pass
        path = request.POST.get('path')

    return redirect(path)


@login_required(login_url='/login')
def friend_requests(request):

    # user = User.objects.all()

    all_r = FriendshipManager.requests(request, request.user)

    context = {
        "all_r": all_r,
        "empty": [],
        "theme": theme,
        "text": text,
    }
    return render(request, 'friends_manager/friend_request.html', context)


@login_required(login_url='/login')
def decline_request(request, id):
    if request.method == 'POST':
        from_user = User.objects.get(id=id)
        try:
            fr = FriendshipRequest.objects.get(from_user=from_user)
            fr.reject()
            fr.delete()
        except Exception as e:
            print(e)
        path = request.POST.get('path')

    return redirect(path)


@login_required(login_url='/login')
def accept_request(request, id):
    if request.method == 'POST':
        from_user = User.objects.get(id=id)
        try:
            fr = FriendshipRequest.objects.get(from_user=from_user)
            fr.accept()
        except:
            pass
        path = request.POST.get('path')

    return redirect(path)


@login_required(login_url='/login')
def remove_friend_confirmation(request, id):
    if request.method == 'POST':
        path = request.POST.get('path')

    context['return_path'] = path
    context['id'] = id

    # return remove_friend(request, id, return_path)
    return render(request, 'user_profiles/remove_friend_confirmation.html', context)


@login_required(login_url='/login')
def remove_friend(request, id):
    if request.method == 'POST':
        other_user = User.objects.get(id=id)
        try:
            FriendshipManager.remove_friend(
                request, from_user=request.user, to_user=other_user)
        except:
            pass
        path = request.POST.get('path')

    return redirect(path)


@login_required(login_url='/login')
def add_follow(request, id):
    if request.method == 'POST':
        other_user = User.objects.get(id=id)
        try:
            FollowingManager.add_follower(request, request.user, other_user)
        except:
            pass
        path = request.POST.get('path')

    return redirect(path)


@login_required(login_url='/login')
def cancel_follow(request, id):
    if request.method == 'POST':
        other_user = User.objects.get(id=id)
        try:
            FollowingManager.remove_follower(request, request.user, other_user)
        except:
            pass
        path = request.POST.get('path')

    return redirect(path)
