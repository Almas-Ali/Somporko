from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from user_profiles import views

admin.site.site_header = 'Somporko Admin'
admin.site.site_title = 'Somporko Admin Panel'
admin.site.index_title = 'Welcome to Somporko Admin Panel'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('newsfeed/', include('user_newsfeed.urls', namespace='newsfeed')),
    path('profile/', include('user_profiles.urls', namespace='profile')),
    path('settings/', include('user_settings.urls', namespace='settings')),
    path('friends/', include('friends_manager.urls', namespace='friends')),
    path('posts/', include('user_post.urls', namespace='posts')),
    path('user/', include('user.urls', namespace='user')),
    path('messages/', include('user_messages.urls', namespace='messages')),
    path('<str:username>/', views.userX, name='profile'),
    path('<str:username>/about', views.aboutX, name='about'),
    # # Password reset urls.
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='reset_password/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password/password_reset_done.html'),
         name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

] 

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
