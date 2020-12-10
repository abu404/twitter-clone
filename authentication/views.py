from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib import auth
import jwt
from django.conf import settings


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not request.data:
            raise ValidationError({"body": "Request body is missing"})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if username is None or password is None:
            return Response({
                'errors': ["Email/Password is missing"]
            }, status=status.HTTP_400_BAD_REQUEST)
        user = auth.authenticate(username=username, password=password)
        print("user", user)
        if user:
            auth_token = jwt.encode(dict(username=username), settings.JWT_SECRET)
            serializer = UserSerializer(user)
            response_data = {**serializer.data, **dict(token=auth_token)}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({"errors": "Username / Password does not match"}, status=status.HTTP_400_BAD_REQUEST)