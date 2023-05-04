from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from home.models import Home_About
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from user_profiles.models import ManageProfile, ProfilePost, UserDetail
from user_settings.models import Delete_Request, UserPrivacy
from home.models import Report
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def index(request):
    if request.user.is_anonymous == False:
        return redirect('/newsfeed')
    home = Home_About.objects.all().first()
    context = {
        "home": home,
    }
    return render(request, 'home/index.html', context)


def loginUser(request):
    if request.user.is_anonymous == False:
        return redirect('/newsfeed')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            username = User.objects.get(email=email.lower()).username
            user = authenticate(username=username, password=password)
        except:
            user = None
            messages.warning(request, 'Incorrect email or password !')
            # return redirect('/login')
        if user is not None:
            try:
                # If account delete request exist then delete the delete request.
                delete = Delete_Request.objects.get(user=username)
                if username == delete.user:
                    delete.delete()
            except:
                pass
            userDetail = request.META.get('HTTP_USER_AGENT')
            UserDetail(sno=username, value=userDetail).save()
            login(request, user)
            # messages.success(request, 'You have sucessfully logged in !')
            return redirect('/newsfeed')
        else:
            messages.warning(request, 'Incorrent Email or Password  !')
            return render(request, 'home/login.html')
        messages.success(request, 'You have successfully login !')
    return render(request, 'home/login.html')


def logoutUser(request):
    logout(request)
    return redirect('/login')


def UserMesseges(request):
    return render(request, 'messeges.html')


def register(request):
    if request.user.is_anonymous == False:
        return redirect('/newsfeed')
    elif request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = email.split('@')[0]
        password1 = request.POST['password']
        password2 = request.POST['repassword']

        try:
            a = User.objects.get(email=email)
        except:
            a = None

        if len(fname) <= 2:
            messages.warning(
                request, 'Please write a valid name for your account !')
        elif len(lname) <= 2:
            messages.warning(
                request, 'Please write a valid name for your account !')
        elif len(password1) < 7:
            messages.warning(
                request, 'Password must contain lest 8 charecter !')
        elif a is not None:
            messages.warning(request, 'Email already exists !')
        elif password1 != password2:
            messages.warning(request, 'Your passwords didn\'t matched !')
        else:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists !')
            else:
                set_user = User.objects.create_user(
                    username=username, email=email, password=password1, first_name=fname, last_name=lname)
                set_user.save()
                ManageProfile(sno=set_user).save()
                ProfilePost(sno=set_user, is_profile_img=True).save()
                UserPrivacy(user=set_user).save()

                messages.success(
                    request, 'Your account has been created successfully !')

    return render(request, 'home/register.html')


def report(request):
    if request.user.is_anonymous == False:
        return redirect('/newsfeed')
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        msg = request.POST.get('msg')
        contact = Report(name=name, email=email, phone=phone,
                         msg=msg, date=datetime.now())
        contact.save()
        messages.success(request, 'Your report has been sent !')
    return render(request, 'home/report.html')


@login_required(login_url='/login')
@csrf_exempt
def userSearch(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if len(query) <= 1 or len(query) >= 20:
            userq = None
            userInfo = None
            userInfoPic = None
        else:
            user_query = User.objects.filter(
                Q(first_name__icontains=query.lower()) |
                Q(last_name__icontains=query.lower()) | 
                Q(username__icontains=query.lower()) |
                Q(email__icontains=query.lower())
            ).distinct().order_by('id')

            userInfo = ManageProfile.objects.all()
            # userInfoPic = ProfileImageUser.objects.all().order_by('-time')


            if user_query.count() == 0:
                user_query = None
                userInfo = None
                userInfoPic = None

    context = {
        "userq": user_query,
        "userInfo": userInfo,
        # "userInfoPic": userInfoPic,
    }
    return render(request, 'news_feed/search.html', context)


def forget_password(request):
    return render(request, 'home/forget_password.html')


def email_search_reset(request):
    context = {}

    if request.method == 'POST':
        email = request.POST.get('email')

        usr = User.objects.filter(email=email).first()
        context['usr'] = usr

        img = ProfilePost.objects.filter(sno=usr).order_by('-created').first()
        context['img'] = img

    else:
        return redirect('/login')

    return render(request, 'home/email_search_reset.html', context)
