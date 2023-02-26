from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin

from .models import MyUser, BloodTypeRezus, BloodTypeGroup, BloodType


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ("email",)


class MyUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MyUser
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(MyUser)
admin.site.register(BloodTypeRezus)
admin.site.register(BloodTypeGroup)
admin.site.register(BloodType)
