from django.contrib import admin
from django.contrib.auth.models import Group
from apps.account.forms import UserChangeForm, UserCreationForm
from apps.account.models import Role, User, UserPreferences, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    verbose_name = "Profile"
    can_delete = False
    extra = 0
    exclude = ["deleted_at"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    inlines = [UserProfileInline]
    list_display = ["email", "role", "state", "is_profile_set"]
    readonly_fields = ["created_at", "updated_at", "last_login", "role", "date_joined"]
    exclude = ["deleted_at", "user_permissions", "groups"]
    list_filter = ["role", "is_profile_set"]
    search_fields = ["email"]
    ordering = ["-created_at"]
    filter_horizontal = []
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


admin.site.register(Role)
admin.site.register(UserPreferences)

# since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
