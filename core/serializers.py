from django.contrib.auth.models import User
from rest_framework import serializers


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username","email","password"]

    def create(self,validated_date):
        user = User.objects.create_user(
            username = validated_date["username"],
            email=validated_date["email"],
            password=validated_date["password"]
        )
        return user