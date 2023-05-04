from datetime import datetime
from django.contrib.sitemaps import Sitemap
from django.contrib.auth.models import User
from django.urls import reverse
# from pages.models import Page


class UserSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return User.objects.all()

    def lastmod(self, obj):
        # return datetime.strptime(str(obj.last_login), '%Y-%m-%d %H:%M:%S.%f +%H:%M').year
        return obj.date_joined.date()

    def location(self, obj):
        return '/%s' % (obj.username)


# class PageSitemap(Sitemap):
#     changefreq = "hourly"
#     priority = 0.8
#     protocol = 'http'

#     def items(self):
#         return Page.objects.all()

#     def lastmod(self, obj):
#         return obj.date

#     def location(self, obj):
#         return '/pages/%s' % (obj.id)


class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return ['home:index_home', 'home:login', 'home:register', 'home:report']

    def location(self, item):
        return reverse(item)
