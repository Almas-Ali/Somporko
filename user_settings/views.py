from django.shortcuts import render, redirect
from user_profiles.models import ManageProfile, ProfilePost
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from user_settings.models import UserPrivacy, Delete_Request
from django.contrib.auth.models import User


@login_required(login_url='/login')
def settings(request):
    return render(request, 'user_settings/settings.html')


@login_required(login_url='/login')
def general_settings(request):
    settingsUser = ManageProfile.objects.filter(sno=request.user).first()
    gender = settingsUser.gender
    if gender == 'Male':
        value1 = 'checked'
    else:
        value1 = ''

    if gender == 'Female':
        value2 = 'checked'
    else:
        value2 = ''

    if gender == 'Other':
        value3 = 'checked'
    else:
        value3 = ''

    birthday = settingsUser.birthday.isoformat()

    context = {
        "settingsUser": settingsUser,
        "value1": value1,
        "value2": value2,
        "value3": value3,
        "birthday": birthday,
    }
    return render(request, 'user_settings/general_settings.html', context)


@login_required(login_url='/login')
def settings_bio(request):
    settingsUser = ManageProfile.objects.filter(sno=request.user).first()
    context = {
        "settingsUser": settingsUser,
    }

    if request.method == 'POST':
        try:
            bio = request.POST.get('bio')
            address = request.POST.get('address')
            religion = request.POST.get('religion')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            birthday = request.POST.get('birthday')
            setting = ManageProfile(
                bio=bio, religion=religion, gender=gender, phone=phone, address=address, birthday=birthday, sno=request.user)
            setting.save()
            messages.success(request, 'Your profile has been updated !')
            return redirect('/settings')
        except:
            messages.error(request, 'Please fill all those fields correctly.')

        return render(request, 'user_settings/general_settings.html', context)

    return render(request, 'home/404.html', context)


# @login_required(login_url='/login')
# def settings_img(request):
#     settingsUser = ManageProfile.objects.filter(sno=request.user).first()
#     context = {
#         "config": config,
#         "settingsUser": settingsUser,
#     }

#     if request.method == 'POST':
#         profileImg = request.POST.get('profileImg')
#         setting = ManageProfile(profileImg=profileImg,
#                                 sno=request.user)
#         setting.save()
#         messages.success(request, 'Your profile has been updated !')

#         return render(request, 'user_settings/settings.html', context)

#     return render(request, 'home/404.html', context)


@login_required(login_url='/login')
def request_delete(request):
    if request.method == 'POST':
        password = request.POST['password']
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            Delete_Request(user=request.user, email=request.user.email).save()
            messages.success(
                request, 'Your deleting request has been sent to server !\nYour account will be permanently deleted after 30 days.\n If you want to get back then login again. ')
            return redirect('/logout')
        else:
            messages.warning(request, 'Wrong username or password !')
            return redirect('/settings/confirm-identity')

    return render(request, 'user_settings/request_delete.html')


@login_required(login_url='/login')
def account(request):
    return render(request, 'user_settings/account_settings.html')


@login_required(login_url='/login')
def imgsettings(request):
    settingsUser = ProfilePost.objects.filter(sno=request.user, is_profile_img=True).order_by('-date').first()
    context = {
        "settingsUser": settingsUser,
    }

    if request.method == 'POST':
        path = request.POST.get('path')
        Img = request.FILES.get('profileImg')
        setting = ProfilePost(sno=request.user, img=Img, is_profile_img=True)
        setting.save()
        messages.success(request, 'Your profile picture has been updated !')
        return redirect(f'{path}')

    return render(request, 'user_settings/profile_set.html', context)


@login_required(login_url='/login')
def privacy(request):
    settings = UserPrivacy.objects.filter(user=request.user).first()

    if request.method == 'POST':
        hide_email = request.POST.get('hide_email')
        hide_phone = request.POST.get('hide_phone')
        hide_friends = request.POST.get('hide_friends')
        sett = UserPrivacy(hide_email=hide_email,
                           hide_phone=hide_phone, hide_friends=hide_friends, user=request.user)
        sett.save()
        messages.success(request, 'Your privacy settings has been updated !')
        return redirect('/settings')

    if settings.hide_email == 'Yes':
        value1 = 'checked'
    else:
        value1 = ''

    if settings.hide_email == 'No':
        value2 = 'checked'
    else:
        value2 = ''

    if settings.hide_phone == 'Yes':
        value3 = 'checked'
    else:
        value3 = ''

    if settings.hide_phone == 'No':
        value4 = 'checked'
    else:
        value4 = ''

    if settings.hide_friends == 'Yes':
        value5 = 'checked'
    else:
        value5 = ''

    if settings.hide_friends == 'No':
        value6 = 'checked'
    else:
        value6 = ''

    context = {
        "settings": settings,
        "value1": value1,
        "value2": value2,
        "value3": value3,
        "value4": value4,
        "value5": value5,
        "value6": value6,
    }
    return render(request, 'user_settings/privacy.html', context)


@login_required(login_url='/login')
def security(request):
    userInfo = User.objects.get(username=request.user)
    context = {
        "userInfo": userInfo,
    }
    return render(request, 'user_settings/security.html', context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        pp = request.POST.get('passwordP')
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')
        l = request.POST.get('logout')

        user = authenticate(username=request.user, password=pp)
        if user is not None:
            if p1 != p2:
                messages.warning(request, 'Password not matched !')
            else:
                # user.set_password(request.user, raw_password=p2)
                user.set_password(p2)
                user.save()
                messages.success(request, 'Password changed successfully !')

                if l == 'on':
                    return redirect('/logout')
                elif l == 'None':
                    return redirect('/settings')
        else:
            messages.warning(request, 'Wrong password !')

    return render(request, 'user_settings/change_password.html')


@login_required(login_url='/login')
def confirm_identity(request):
    # if request.method == 'POST':
    #     password = request.POST.get('password')

    #     user = authenticate(username=request.user, password=password)

    #     if user is not None:
    #         return redirect('/settings/request-delete')
    #     else:
    #         messages.warning(request, 'Wrong password !')


    return render(request, 'user_settings/confirm_delete.html')
