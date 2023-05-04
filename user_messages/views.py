from django.shortcuts import render
from user_messages.models import UserMessages
from user_profiles.models import User

theme = 'light'
text = 'dark'
navbar = 'primary'
theme, text = text, theme


def get_ip(request):
    '''User IP catcher.'''
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        ip = forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def message(request):
    user = request.user
    
    msg_get = UserMessages.objects.filter(to_user=user)
    msg_sent = UserMessages.objects.filter(from_user=user)
    msgs = msg_get.union(msg_sent)

    msgss = []
    for msg in msgs:
        print(msg)
        if msg.from_user or msg.to_user not in msgss.from_user or msgss.to_user:
            msgss.append(msg)
    print(msgss)

    context = {
        "theme": theme,
        "text": text,
        "msgs": msgs,
    }
    return render(request, 'user_messages/inbox.html', context)


def chat_box(request, id):
    if request.method == 'POST':
        msg = request.POST.get('msg_box')
        user = User.objects.get(id=id)
        umsg = UserMessages(from_user=request.user, to_user=user, msg=msg, ip=get_ip(request))
        umsg.save()

    user = User.objects.get(id=id)
    msg1 = UserMessages.objects.filter(from_user=user, to_user=request.user)
    msg2 = UserMessages.objects.filter(from_user=request.user, to_user=user)
    msgs = msg1.union(msg2).order_by('time')

    context = {
        'msgs': msgs,
        'user': user
    }
    return render(request, 'user_messages/chat_box.html', context)
