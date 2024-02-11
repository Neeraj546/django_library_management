from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from library.models import Book
from library.serializers.book_serializer import BookSerializer
from rest_framework.permissions import IsAuthenticated

class ListBookView(APIView):
    def get(self, request):
        books = Book.objects.all().order_by('-updated_at')
        serializer = BookSerializer(books, many=True)
        return Response({"books": serializer.data}, status=status.HTTP_200_OK)
    
class CreateBookView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        print(request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"message": "Book Created", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        book = Book.objects.filter(id=id).first()
        if not book:
            return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book, data=request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"message": "Book Updated", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        book = Book.objects.filter(id=id).first()
        if not book:
            return Response({"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response({"message": "Book Deleted"}, status=status.HTTP_200_OK)