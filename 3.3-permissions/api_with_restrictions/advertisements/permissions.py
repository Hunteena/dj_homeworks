from rest_framework.permissions import BasePermission


class IsCreatorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator or request.user.is_staff
