from rest_framework.permissions import BasePermission,DjangoModelPermissions

class CustomDjangoModelPermissions(DjangoModelPermissions):
   perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

class HasPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perms(view.permissions)


class HasAnyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_any_perms(
            view.permissions
        )
