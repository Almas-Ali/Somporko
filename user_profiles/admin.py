from django.contrib import admin
from user_profiles.models import ManageProfile, ProfilePost, Comment, UserDetail, User, ProfileImage


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'sno', 'user', 'parent', 'time')
    list_filter = ('user', 'time')
    search_fields = ('post', 'cmt', 'user', 'parent', 'time')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('id', 'username', 'email', 'first_name',
                     'last_name', 'is_staff', 'is_active')

    ordering = ('-date_joined', 'last_login')
    filter_horizontal = ()
    fieldsets = ()
    readonly_fields = ('date_joined', 'last_login')
    list_per_page = 100


admin.site.register(User)
admin.site.register(ManageProfile)
admin.site.register(ProfilePost)
admin.site.register(ProfileImage)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserDetail)
