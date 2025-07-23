from django.contrib.auth import get_user_model
from django.db import models
import uuid



User = get_user_model()

class Room(models.Model):
    ROOM_TYPES = (
        ('chat', 'Chat'),
        ('video', 'Video'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='chat')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_by']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.room_type})"


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



    class Meta:
        indexes = [
            models.Index(fields=['room', 'timestamp']),
            models.Index(fields=['sender']),
        ]
        ordering = ['timestamp']  # chronological message order

    def __str__(self):
        return f"From {self.sender.username} in {self.room.name} at {self.timestamp}"
    
class RoomParticipant(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('room', 'user')  # Prevent duplicate entries
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.username} in {self.room.name}"

