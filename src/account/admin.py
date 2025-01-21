from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UserProfile, CustomUser, UserFollowerModel, ForgotPasswordTokenModel

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("fullname",)}),
        (_("Permissions"), {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "fullname", "password1", "password2", "is_staff",
                "is_active", "is_superuser",
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    readonly_fields = ("date_joined",)


admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['birthday', 'profile_pic']
    search_fields = ['birthday'] 
    list_filter = ['birthday']


@admin.register(UserFollowerModel)
class UserFollowerAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following']
    search_fields = ['follower', 'following'] 
    list_filter = ['created_at']

@admin.register(ForgotPasswordTokenModel)
class ForgotPasswordAdmin(admin.ModelAdmin):
    list_display = ['user__fullname', 'created_at', 'expired_at']
    search_fields = ['user__fullname'] 
    list_filter = ['created_at', 'expired_at']



