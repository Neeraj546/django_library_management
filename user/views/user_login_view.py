from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.serializers.user_serializer import UserLoginSerializer
from user.models import User
from django.contrib.auth import authenticate
from user.views.user_token_view import UserToken

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        token = UserToken.get_tokens_for_user(user)
        return Response({"message": "User Login Successful", "token": token}, status=status.HTTP_200_OK)