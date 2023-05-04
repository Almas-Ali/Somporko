from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from user_profiles.models import ProfilePost, ManageProfile, Comment
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



@csrf_exempt
@login_required(login_url='/login')
def post(request, username, id):

    user = User.objects.get(username=username)
    if user == None:
        return redirect('/')

    userInfo = ManageProfile.objects.get(sno=user)
    userInfoPic = ProfilePost.objects.filter(
        sno=user, is_profile_img=True).first()
    userInfoPicAll = ProfilePost.objects.all().order_by('-date')

    if request.method == 'POST':
        post = request.POST.get('post')
        # photo = request.POST.get('photo')
        user_post = ProfilePost(
            post=post, sno=user.get_full_name(), username=user.username)
        user_post.save()

    post = ProfilePost.objects.get(id=id)

    comments = Comment.objects.filter(post=post, parent=None)
    replies = Comment.objects.filter(post=post).exclude(parent=None)

    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    # print(replyDict)

    context = {
        "userInfo": userInfo,
        "user": user,
        "userInfoPic": userInfoPic,
        "userInfoPicAll": userInfoPicAll,
        "post": post,
        "comments": comments,
        "replies": replyDict
    }

    return render(request, 'user_post/post.html', context)
