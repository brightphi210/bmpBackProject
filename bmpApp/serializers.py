from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["name"] = user.name
        token["email"] = user.email
        
        token["profile_pic"] = user.profile_pic.url if user.profile_pic else None

        userProfile = UserProfile.objects.filter(user=user).first()
        token['id'] = userProfile.id if userProfile else None

        return token


class UserProfileSerializer(ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'id', 'profile_pic',]
        depth = 1


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
