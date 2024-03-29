from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.serializers.user_serializer import UserSerializer, ChangePasswordSerializer, ResetPasswordEmailSerializer, ResetPasswordSerializer
from rest_framework.permissions import IsAuthenticated

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
    
class SendResetPasswordEmail(APIView):
    def post(self, request):
        serializer = ResetPasswordEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Mail sent with the reset password link"}, status=status.HTTP_200_OK)
    
class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
    
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        request.user.auth_token.delete()
        return Response({"message": "User Logout Successful"}, status=status.HTTP_200_OK)
