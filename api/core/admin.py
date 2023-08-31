from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            # Remove build in delete action on admin panel.
            del actions["delete_selected"]
        return actions

    fields = (
        "first_name",
        "last_name",
        "email",
        "country",
        "department",
        "manager",
        "is_active",
        "groups",
        "user_permissions",
    )
    list_display = (
        "email",
        "get_full_name",
        "department",
        "is_active",
    )
    list_filter = (
        "department",
        "is_active",
        "country"
    )
    autocomplete_fields = ("manager",)
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    ordering = ("email",)

    def has_delete_permission(self, request, obj=None) -> bool:
        """
        Prevent users from deleting on admin panel.
        """
        return False


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    fields = ("name", "parent")
    list_display = ("name", "parent")
