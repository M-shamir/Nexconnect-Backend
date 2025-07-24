import re
from rest_framework.exceptions import ValidationError
from chat.models import Room

def validate_room_name(name, user):
    if not user or not user.is_authenticated:
        raise ValidationError("User must be authenticated.")
    if not name or not name.strip():
        raise ValidationError("Room name is required.")
    name = name.strip()
    if len(name) < 3:
        raise ValidationError("Room name must be at least 3 characters long.")
    if len(name) > 50:
        raise ValidationError("Room name must not exceed 50 characters.")
    if not re.search(r'[a-zA-Z]', name):
        raise ValidationError("Room name must contain at least one alphabet character.")
    if Room.objects.filter(name=name, created_by=user).exists():
        raise ValidationError("You already have a room with this name.")
    return name

def validate_room_type(room_type):
    from chat.models import Room
    valid_types = dict(Room.ROOM_TYPES).keys()
    if room_type not in valid_types:
        raise ValidationError(f"Room type must be one of: {', '.join(valid_types)}.")
    return room_type
