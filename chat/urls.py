from django.urls import path
from .views import *

urlpatterns = [
    path('rooms/',ChatRooms.as_view(),name='chat-rooms'),
    path('rooms/<uuid:room_id>',RoomDetailView.as_view(),name='room-detail-view'),    
]