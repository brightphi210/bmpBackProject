from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from . models import *
from . serializers import *

from rest_framework import status

# Create your views here.


@api_view(['GET'])
def endpoint(request):
    data = {
        'Enpoint' : 'api/'
    }
    return Response(data)


class GetAndCreateUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):

        email = request.data.get('email', None)

        # Check if a user with the given email already exists
        if email and User.objects.filter(email=email).exists():

            user = User.objects.get(email=response.data['email'])

            send_email_confirmation(user.email)

            return Response({'message': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        response = super().create(request, *args, **kwargs)
        
        # Check if the creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            # Registration failed, customize the error message
            error_message = {'message': 'User registration failed. Please check the provided data.'}
            response.data = error_message
            return response