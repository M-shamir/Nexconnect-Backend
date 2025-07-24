from django.contrib.auth.models import User
from rest_framework import serializers
from core.validators.user_validators import validate_username, validate_email, validate_password

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username","email","password"]

    def validate_username(self, value):
        validate_username(value)
        return value

    def validate_email(self, value):
        validate_email(value)
        return value

    def validate_password(self, value):
        validate_password(value)
        return value
    

    def create(self,validated_date):
        user = User.objects.create_user(
            username = validated_date["username"],
            email=validated_date["email"],
            password=validated_date["password"]
        )
        return user