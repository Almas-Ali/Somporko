from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user_profiles.models import Comment
from user_profiles.models import ProfilePost


theme = 'light'
text = 'dark'
navbar = 'primary'
theme, text = text, theme


@login_required(login_url='/login')
def user_menu(request):
    return render(request, 'user/user_menu.html')


@login_required(login_url='/login')
def notifications(request):
    context = {
        "theme": theme,
        "text": text,
    }
    return render(request, 'user/notifications.html', context)


@login_required(login_url='/login')
def post_comment(request):
    if request.method == 'POST':
        user = request.user
        cmt = request.POST.get('comment')
        path = request.POST.get('path')
        post = request.POST.get('post')
        post = ProfilePost.objects.get(id=post)
        try:
            cm = Comment(user=user, cmt=cmt, post=post)
            cm.save()
        except:
            pass
        path = request.POST.get('path')

        return redirect(f'{path}#{post}')
    else:
        return redirect('/')


@login_required(login_url='/login')
def post_comment_reply(request):
    if request.method == 'POST':
        user = request.user
        cmt_no = request.POST.get('comment')
        reply = request.POST.get('reply')
        path = request.POST.get('path')
        post = request.POST.get('post')

        post = ProfilePost.objects.get(id=post)
        cmt_no = Comment.objects.get(sno=cmt_no)
        
        try:
            cm = Comment(user=user, cmt=reply, post=post, parent=cmt_no)
            cm.save()
        except:
            pass
        path = request.POST.get('path')

        return redirect(f'{path}#{post}')
    else:
        return redirect('/')
