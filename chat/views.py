from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404 
from .serializers import RoomSerializer
from .models import Room
# Create your views here.



class ChatRooms(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        room_name  = request.data.get('room_name')
        room_type = request.data.get('room_type','chat')
        created_by = request.user

        if not room_name:
            return Response({"error":"Room name is required"},status=status.HTTP_400_BAD_REQUEST)

        room  = Room.objects.create(
            name=room_name,
            created_by= created_by,
            room_type = room_type
        )
        serializer = RoomSerializer(room)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    


    def get(self,request,*args,**kwargs):
        chat_rooms = Room.objects.filter(room_type='chat')
        serializer = RoomSerializer(chat_rooms,many=True)
        return Response(serializer.data)
    
class RoomDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,room_id,*args,**kwargs):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error":"Room Not found"},status=status.HTTP_400_BAD_REQUEST)

        serializer = RoomSerializer(room)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    

    
    