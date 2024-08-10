
# Create your views here.

from rest_framework import generics
from .models import CustomUser
from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import LoginSerializer, UserSerializer

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer