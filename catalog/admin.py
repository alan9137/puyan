from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'phone', 'email', 'code')


@admin.register(UserSet)
class UserSetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name')


@admin.register(Pressure)
class PressureAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recorded_at')


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recorded_at')


@admin.register(Sugar)
class SugarAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recorded_at')


@admin.register(A1c)
class SugarAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recorded_at')


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recorded_at')


@admin.register(Default)
class DefaultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


@admin.register(UserSetting)
class UserSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


@admin.register(Medical)
class UserSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'inviter', 'invitees')


@admin.register(Care)
class CareAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')


@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recorded_at')
