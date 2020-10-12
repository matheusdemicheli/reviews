from django.shortcuts import render
from rest_framework import permissions, serializers, viewsets
from api.models import Review
from api.serializers import ReviewSerializer
from api.permissions import IsReviewer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Reviews to be viewed or posted.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated & IsReviewer]

    def get_queryset(self):
        """
        Returns only Reviews made by the logged user.
        """
        user = self.request.user
        return user.reviewer.review_set.all().order_by('pk')
