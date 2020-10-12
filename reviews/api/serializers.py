from rest_framework import serializers
from api.models import Review
from api.utils import get_client_ip


class ReviewSerializer(serializers.ModelSerializer):
    """
    Review ModelSerializer.
    """
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['reviewer', 'ip_address']

    def create(self, validated_data):
        """
        Overrided to set some metadata values to the instance.
        """
        request = self.context['request']
        validated_data.update({
            'reviewer': request.user.reviewer,
            'ip_address': get_client_ip(request),
        })
        return super().create(validated_data)
