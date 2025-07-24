from rest_framework import serializers
from .models import  Room
from chat.Validation.room_validation import validate_room_name, validate_room_type


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'room_type', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

    def validate_name(self, value):
        user = self.context['request'].user
        return validate_room_name(value, user)

    def validate_room_type(self, value):
        return validate_room_type(value)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)