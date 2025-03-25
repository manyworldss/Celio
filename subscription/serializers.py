from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    is_premium = serializers.BooleanField(read_only=True)
    class Meta:
        model = Subscription
        fields = ['plan', 'status', 'start_date', 'end_date', 'is_premium']
        read_only_fields = fields
        