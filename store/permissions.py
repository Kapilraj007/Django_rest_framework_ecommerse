from rest_framework import permissions

class ViewCustomerHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')
    
class IsVendorOrAdmin(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'vendor') and request.user == obj.vendor:
            return True
        
        return False

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)