from django.contrib import admin
from django.urls import path, include
from home import views
from django.contrib.sitemaps.views import sitemap
from home.sitemaps import UserSitemap, StaticSitemap #, PageSitemap
from django.views.generic.base import TemplateView


app_name = "home"
# handler404 = 'home.views.handler404'

sitemaps = {
    'user': UserSitemap,
    # 'page': PageSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    # path('404', views.handler404, name='handler404'),
    # path('auto-suggest', views.auto_suggest, name='auto_suggest'),
    path('somporko-site-sitemap-416945.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),

    path('', views.index, name='index_home'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.register, name='register'),
    path('report', views.report, name='report'),
    path('search', views.userSearch, name='search'),
    path('forget-password', views.forget_password, name='forget-password'),
    path('email-search-reset', views.email_search_reset, name='email-search-reset'),
]
