from django.contrib import admin
from user_settings.models import UserPrivacy, Delete_Request, VerifyUser

# Register your models here.

admin.site.register(UserPrivacy)
admin.site.register(Delete_Request)
admin.site.register(VerifyUser)
