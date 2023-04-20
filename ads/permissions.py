from rest_framework.permissions import BasePermission
from users.models import User


class IfOwner(BasePermission):
    message = "Редактировать и удалять может только создатель подборки"

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "owner"):
            if request.user == obj.owner:
                return True
            return False
        if hasattr(obj, "author"):
            if request.user == obj.author:
                return True
            return False


class IfStaff(BasePermission):
    message = "Редактировать и удалять может только создатель или модератор!"

    def has_permission(self, request, view):
        if request.user.role in [User.MODERATOR, User.ADMIN]:
            return True
        return False
