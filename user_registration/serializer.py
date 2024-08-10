from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'firstName', 'lastName', 'email', 'password', 'dob', 'address', 'phonenumber']

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            dob=validated_data['dob'],
            address=validated_data['address'],
            phonenumber=validated_data['phonenumber'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials provided.')
        else:
            raise serializers.ValidationError('Both email and password are required.')

        data['user'] = user
        return data
