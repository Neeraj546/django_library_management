from rest_framework import serializers
from user.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from user.utils import Utils

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
        if not User.objects.filter(email=data['email'], is_confirmed=True).exists():
            raise serializers.ValidationError("User Confirmation Pending")
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
    
class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ('email',)

    def validate(self, data):
        email = data.get('email')
        if not User.objects.filter(email=email).exists():
            serializers.ValidationError("there's no user registered with this email")
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        link = "http://localhost:8000/api/user/reset-password/" + uid + "/" + token
        email_body = "Please click the link below to reset your account password\n" + link
        data = {
            "subject": "Reset Account Password | Library Management",
            "to_email": user.email,
            "body": email_body
        }
        Utils.send_email(data)
        return data
    
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, max_length=255)
    confirm_password = serializers.CharField(required=True, max_length=255)

    class Meta:
        fields = ('new_password', 'confirm_password')
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password does not match")
        uid = self.context.get('uid')
        token = self.context.get('token')
        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Invalid Token")
            user.set_password(data['new_password'])
            user.save()
        except DjangoUnicodeDecodeError as identifier:
            raise serializers.ValidationError("Invalid Token")
        return data
        
