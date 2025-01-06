from rest_framework import permissions
class IsArticleAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

          # Check if the user is the author of the comment
        if obj.author != request.user:
            return False
        
        return True

    


class IsCommentAuthorOrReadOnly(permissions.BasePermission):

    # Custom permission to only allow the author of a comment to update or delete it.

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) to everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user is the author of the comment
        if obj.user != request.user:
            return False
        
        return True
