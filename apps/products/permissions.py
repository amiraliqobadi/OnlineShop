from rest_framework import permissions


class ProductsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user.products_manager:
            return True
        return obj.owner == request.user
