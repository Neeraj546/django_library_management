from rest_framework import serializers
from user.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'contact', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            contact=validated_data['contact'],
            password=validated_data['password']
        )
        return user
    
    def validate(self, data):
        if not data['contact'].isdigit():
            raise serializers.ValidationError("Contact should be a number")
        return data
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ('email', 'password')
    
    def validate(self, data):
        if not User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("User does not exist")
        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'contact')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=255)
    new_password = serializers.CharField(required=True, max_length=255)
    confirm_password = serializers.CharField(required=True, max_length=255)

    class Meta:
        fields = ('old_password', 'new_password', 'confirm_password')
    
    def validate(self, data):
        user = self.context.get('request').user
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password does not match")
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError("Old password is incorrect")
        user.set_password(data['new_password'])
        user.save()
        return data