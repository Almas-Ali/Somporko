from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from home.models import Report
from user_profiles.models import ManageProfile, ProfilePost, Comment
from django.contrib.auth.models import User
from user_settings.models import UserPrivacy, VerifyUser
from django.views.decorators.csrf import csrf_exempt
from friendship.models import Friend, Follow, Block, FriendshipRequest, FollowingManager, FriendshipManager


# @login_required(login_url='/login')


def user_profiles(request, id):

    user = User.objects.get(id=id)
    if user == None:
        return HttpResponse(f'404 - \"{user}\" User Not found !')

    userInfo = ManageProfile.objects.filter(sno=user).first()
    userInfoPic = ProfilePost.objects.filter(
        sno=user, is_profile_img=True).order_by('-date').first()
    try:
        all_r = FriendshipManager.requests(request, request.user)
    except:
        all_r = []

    if request.method == 'POST':
        post = request.POST.get('post')
        photo = request.POST.get('photo')
        user_post = ProfilePost(
            post=post, sno=request.user.username, img=photo)
        user_post.save()

    posts = ProfilePost.objects.filter(
        sno=user).order_by('-date')

    # profile = ProfileImageUser.objects.filter(sno=user)

    # posts = profile.union(postx).all().order_by('-date')
    # print('\n\n\n\n')
    # for post in posts:
    #     print(post.img)
    # print('\n\n\n\n')

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

    try:
        if FriendshipRequest.objects.filter(
            from_user=user, to_user=request.user
        ).exists():
            recevied_request = True
        else:
            recevied_request = False
    except:
        recevied_request = False

    try:
        veri = VerifyUser.objects.get(user=user)
    except:
        veri = False

    comment = Comment.objects.all()

    context = {
        "userInfo": userInfo,
        "user": user,
        "userInfoPic": userInfoPic,
        "posts": posts,
        "is_friend": is_friend,
        "is_following": is_following,
        "is_sent_request": is_sent_request,
        "total_follow": total_follow,
        # "requested_user": requested_user,
        "veri": veri,
        "comments": comment,
        # 'profile': profile,
        'recevied_request': recevied_request,
    }
    return render(request, 'user_profiles/profile.html', context)


def userX(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponse('404 User Not Found !')
    return user_profiles(request, user.id)


@login_required(login_url='/login')
def about(request, id):

    user = User.objects.get(id=id)
    userInfoPic = ProfilePost.objects.filter(
        sno=user, is_profile_img=True).order_by('-date').first()
    setting = UserPrivacy.objects.get(user=user)
    hide_email = setting.hide_email
    hide_phone = setting.hide_phone
    all_r = FriendshipManager.requests(request, request.user)

    if user == None:
        return HttpResponse('404 - Not found !')

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


    try:
        veri = VerifyUser.objects.get(user=user)
    except:
        veri = False

    userInfo = ManageProfile.objects.filter(sno=user).first()
    context = {
        "userInfo": userInfo,
        "user": user,
        "userInfoPic": userInfoPic,
        "hide_email": hide_email,
        "hide_phone": hide_phone,
        "is_friend": is_friend,
        "is_following": is_following,
        "is_sent_request": is_sent_request,
        "total_follow": total_follow,
        # "requested_user": requested_user,
        "veri": veri,
        "empty": [],
    }
    return render(request, 'user_profiles/about.html', context)


def aboutX(request, username):
    user = User.objects.get(username=username)
    return about(request, user.id)


@login_required(login_url='/login')
def report(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        msg = request.POST.get('msg')
        report = Report(name=name, email=email, phone=phone,
                        msg=msg, date=datetime.now())
        report.save()
        messages.success(request, 'Your report has been sent !')
    return render(request, 'user_profiles/report.html')


# def not_exist(request):
#     return HttpResponse('404 - Not found !')

@login_required(login_url='/login')
@csrf_exempt
def likepost(request):
    if request.method == 'GET':
        post_id = request.GET.get('post_id')
        path = request.GET.get('path')
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

    return redirect(f'{path}#{post_id}')


@login_required(login_url='/login')
@csrf_exempt
def likecomment(request):
    if request.method == 'GET':
        cmt_id = request.GET.get('comment_id')
        path = request.GET.get('path')
        post_obj = Comment.objects.get(sno=cmt_id)

        if request.user in post_obj.likes.all():
            post_obj.likes.remove(request.user)
        else:
            post_obj.likes.add(request.user)

    return redirect(f'{path}#{cmt_id}')
