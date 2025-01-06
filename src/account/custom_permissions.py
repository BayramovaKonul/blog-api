from rest_framework import permissions

class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the author of a comment to update or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) to everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user is the author of the comment
        if obj.user != request.user:
            return False
        
        return True
