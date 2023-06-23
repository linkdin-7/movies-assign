from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

'''
Serializer for User Data

'''
class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username', 'password','token']

    #create refresh and access token post registration/login
    def get_token(self,user):
        print(user)
        refresh = RefreshToken.for_user(user)
        return {
        'access_token': str(refresh.access_token)
        }

    #keep password as hash in the database
    def validate_password(self, data):
        return make_password(data)
