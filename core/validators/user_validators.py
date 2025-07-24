import re
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


def validate_username(username: str):
    if len(username.strip()) < 3:
        raise ValidationError("Username must be at least 3 characters long.")
    
    if not re.fullmatch(r"^[a-zA-Z_]+$", username):
        raise ValidationError("Username can only contain letters and underscores. No numbers or special characters allowed.")
    
    if User.objects.filter(username=username).exists():
        raise ValidationError("Username already exists.")


def validate_email(email: str):
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already exists.")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValidationError("Invalid email address.")


def validate_password(password: str):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must include at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must include at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise ValidationError("Password must include at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must include at least one special character.")
