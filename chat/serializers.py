from rest_framework import serializers
from .models import  Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'room_type', 'created_by', 'created_at']