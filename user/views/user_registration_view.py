from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializers.user_serializer import UserRegistrationSerializer
from user.views.user_token_view import UserToken

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        token = UserToken.get_tokens_for_user(user)
        return Response({"message": "User Registration Successful", "token": token},status=status.HTTP_201_CREATED)