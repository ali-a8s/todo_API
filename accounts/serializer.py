from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']  # Fixed: 'password', not 'password1'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_username(self, value):
        if value.lower() == 'admin':  # Case-insensitive just to be safe
            raise serializers.ValidationError("you cant pick admin for username")
        return value

    def validate_email(self, value):
        if 'admin' in value.lower():
            raise serializers.ValidationError("admin cant be in your email")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("passwords must match")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 before creating user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data['username']
        password = data['password']

        if username and password:
            user = authenticate(username= username, password= password)
            if not user:
                raise serializers.ValidationError('username or password is wrong')
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            data['user'] = user
        else:
            raise serializers.ValidationError("Must include username and password.")
        return data
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }