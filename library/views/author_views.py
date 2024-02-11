from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from library.serializers.author_serializer import AuthorSerializer
from rest_framework.permissions import IsAuthenticated

class ListAuthors(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if not request.user.is_admin:
            return Response({"message": "You are not authorized to view this page"}, status=status.HTTP_403_FORBIDDEN)
        authors = User.objects.filter(is_admin=False, is_active=True)
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)