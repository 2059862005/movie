from rest_framework import serializers
from vip.models import vip

class VipCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = vip
        fields = ['id', 'card_name', 'card_price', 'duration', 'info', 'created_at']
