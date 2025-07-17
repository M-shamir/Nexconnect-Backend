from .serializers import UserSignupSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime,timedelta
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
                "message": "Login successful"
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
