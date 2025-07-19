from .serializers import UserSignupSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from datetime import datetime,timedelta
from django.contrib.auth.models import User
# Create your views here.

class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    def post(self,request):
        username = request.data.get('username')
        password  = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token =  str(refresh.access_token)

            expires = datetime.utcnow() + timedelta(minutes=5)

            response = Response({
                "message": "Login successful",
                "user":{
                    id:user.id,
                    "username":user.username,
                    "email":user.email
                }
            }, status=status.HTTP_200_OK)


            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                expires=expires,
                samesite='Lax',
                secure=False  # Set True in production with HTTPS
            )


            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                expires=datetime.utcnow() + timedelta(days=1),
                samesite='Lax',
                secure=False
            )

            return response
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class Refreshtoken(APIView):
    def post(self,request):
        refresh_token = request.cookies.get('refresh_token')
        if not refresh_token:
            return Response({
                "error":"Refresh Token not found"
            })
        try:
            refresh = RefreshToken(refresh_token)
            payload = request.payload
            user_id = payload.get('user_id')

            if not user_id:
                return Response({
                    "error":"Invalid Token payload"
                },status=status.HTTP_401_UNAUTHORIZED)
            try:
                user = User.object.get(id=user_id)
            except:
                raise NotFound("user not found")

            access = refresh.access_token

            expires = datetime.utcnow() + timedelta(hours=2)

            response = Response({
                "message":"Refresh Token Updated",
                "user_id":user.id,
                "user_name" :user.username,
                "email":user.email
            },status=status.HTTP_200_SUCCESS)
            response.set_cookie(
                key="access_token",
                value=access,
                httponly=True,
                expires=expires,
                samesite='Lax',
                secure=False 
            )


            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                expires=datetime.utcnow() + timedelta(days=1),
                samesite='Lax',
                secure=False
            )
            return response
        except TokenError:
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)



