from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.account.forms import UserChangeForm, UserCreationForm
from apps.account.models import Role, User, UserPreferences, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ["email", "role"]
    list_filter = ["role"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Permissions",
            {"fields": ["state", "role"]},
        ),
        ("Important dates", {"fields": ["created_at", "updated_at", "deleted_at"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "state",
                    "role",
                ],
            },
        )
    ]

    search_fields = ["email"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = []


admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(UserPreferences)

# since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
