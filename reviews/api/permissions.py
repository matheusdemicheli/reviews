from rest_framework import permissions


class IsReviewer(permissions.BasePermission):
    """
    Custom permission to only allow Reviewers to see their submited.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user's reviewer is the same of the request.
        """
        return bool(obj.reviewer.user == request.user)
