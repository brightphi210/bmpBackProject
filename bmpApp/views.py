from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.response import Response
from . models import *
from . serializers import *
# from .signals import send_email_confirmation
from .signals import send_email_confirmation

from rest_framework import status

# Create your views here.


@api_view(['GET'])
def endpoint(request):
    data = {
        'Enpoint' : 'api/',
        'GET AND CREATE USER' : 'api/user/',
        'CONFIRM EMAIL':'api/confirm-email/id/'
    }
    return Response(data)






class UserGetCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        # Check if a user with the given email already exists
        if email and User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            send_email_confirmation(user.email)
            return Response({'message': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        response = super().create(request, *args, **kwargs)

        # Check if the creation was successful
        if response.status_code == status.HTTP_201_CREATED:
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            # Registration failed, customize the error message
            error_message = {'message': 'User registration failed. Please check the provided data.'}
            return Response(data=error_message, status=response.status_code)


from django.shortcuts import render, redirect, get_object_or_404

def confirm_email(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    user.is_active= True
    user.save()
    return redirect('https://bmp-app.onrender.com/api/user/')