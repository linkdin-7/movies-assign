# all required imports
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer

# Create your views here.

'''
Creating a Registrantion APIView Class For a New User Registration

'''
class RegisterView(APIView):
    '''
    Registeration of new user using default user model
    '''
    def post(self, request):
        '''
        Get the username and password
        '''
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return token respone
            return Response(serializer.data['token'], status=201)
        return Response(serializer.errors, status=400)