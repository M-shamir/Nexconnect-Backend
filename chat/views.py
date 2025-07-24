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

    def post(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


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
    

    

    
    