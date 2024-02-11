from rest_framework import serializers
from library.models import Library

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ('id', 'name', 'books')

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short")
        if Library.objects.filter(name=value).exists():
            raise serializers.ValidationError("Library with this name already exists")
        return value
