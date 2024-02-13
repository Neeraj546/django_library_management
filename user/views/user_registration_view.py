from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializers.user_serializer import UserRegistrationSerializer
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from user.utils import Utils

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        uid = urlsafe_base64_encode(force_bytes(user.id))
        link = "http://localhost:8000/api/users/confirm/" + uid
        email_body = "Please click the link below to confirm your email\n" + link
        data = {
            "subject": "Confirm Your Email | Library Management",
            "to_email": user.email,
            "body": email_body
        }
        Utils.send_email(data)
        return Response({"message": "Please Confirm Your Email"},status=status.HTTP_201_CREATED)
    
class UserConfirmationView(APIView):
    def get(self, request, uid):
        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)
        except DjangoUnicodeDecodeError as identifier:
            return Response({"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_confirmed:
            return Response({"message": "User already confirmed"}, status=status.HTTP_400_BAD_REQUEST)
        user.confirm_user()
        return Response({"message": "User Confirmed Successfully"}, status=status.HTTP_200_OK)