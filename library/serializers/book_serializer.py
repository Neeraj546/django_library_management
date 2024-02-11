from rest_framework import serializers
from library.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'libraries')

    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("title is too short")
        return value
