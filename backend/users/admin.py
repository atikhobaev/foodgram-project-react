from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Follow


class CustomUserAdmin(UserAdmin):
    list_display = (
        'email', 'username', 'is_active', 'first_name', 'last_name',
    )
    list_filter = ('email', 'username')
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = '-пусто-'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
