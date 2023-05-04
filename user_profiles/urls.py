from django.contrib import admin
from django.urls import path, include
from user_profiles import views
from django.conf import settings
from django.conf.urls.static import static
import os


urlpatterns = [
    path('user/id=<int:id>', views.user_profiles, name='profile'),
    path('about/id=<int:id>', views.about, name='about'),
    path('report', views.report, name='Report'),
    path('likepost', views.likepost, name='likepost'),
    path('likecomment', views.likecomment, name='likecomment'),
] 
#+ static(os.path.join(settings.MEDIA_URL, 'profile'), document_root=os.path.join(settings.MEDIA_ROOT, 'profile'))
