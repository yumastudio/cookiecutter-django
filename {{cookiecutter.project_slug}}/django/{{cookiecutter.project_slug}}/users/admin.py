from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from {{ cookiecutter.project_slug }}.users.forms import UserChangeForm, UserCreationForm
from {{ cookiecutter.project_slug }}.utils.functions import get_photo_preview

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("avatar",)}),) + tuple(
        auth_admin.UserAdmin.fieldsets
    )
    list_display = ["email", "is_superuser", "avatar_preview"]
    search_fields = ["email"]

    def avatar_preview(self, obj):
        return get_photo_preview(
            photo=obj.avatar,
            aspect="1-1",
            width="140"
        )
    avatar_preview.short_description = 'Avatar'
    avatar_preview.allow_tags = True
