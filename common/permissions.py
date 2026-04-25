from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        return request.user and request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    

class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS