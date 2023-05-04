from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user_settings import views

urlpatterns = [
    path('', views.settings, name='settings'),
    path('settings_bio', views.settings_bio, name='settings_bio'),
    # path('settings_img', views.settings_img, name='settings_img'),
    path('general', views.general_settings, name='general_settings'),
    path('request-delete', views.request_delete, name='request-delete'),
    path('account', views.account, name='account'),
    path('imgsettings', views.imgsettings, name='imgsettings'),
    path('privacy', views.privacy, name='privacy'),
    path('security', views.security, name='security'),
    path('change-password', views.change_password, name='change-password'),
    path('confirm-identity', views.confirm_identity, name='confirm-identity'),
]