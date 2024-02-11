from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from library.models import Library
from library.serializers.library_serializer import LibrarySerializer
from rest_framework.permissions import IsAuthenticated

class ListLibraryView(APIView):
    def get(self, request):
        libraries = Library.objects.all().order_by('-updated_at')
        serializer = LibrarySerializer(libraries, many=True)
        return Response({"libraries": serializer.data}, status=status.HTTP_200_OK)
    

class CreateLibraryView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = LibrarySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"message": "Library Created", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        library = Library.objects.filter(id=id).first()
        if not library:
            return Response({"message": "Library not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = LibrarySerializer(library, data=request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"message": "Library Updated", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        library = Library.objects.filter(id=id).first()
        if not library:
            return Response({"message": "Library not found"}, status=status.HTTP_404_NOT_FOUND)
        library.delete()
        return Response({"message": "Library Deleted"}, status=status.HTTP_200_OK)