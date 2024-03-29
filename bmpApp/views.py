from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from . models import *
from . serializers import *
# from .signals import send_email_confirmation
from .signals import send_email_confirmation

from rest_framework import status

# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



@api_view(['GET'])
def endpoint(request):
    data = {
        'Enpoint' : 'api/',
        'GET AND CREATE USER' : 'api/user/',
        'GET, UPDATE, DELETE USER' : 'api/user/id/',
        'GET AND CREATE PROFILE' : 'api/userprofiles',
        'GET, UPDATE AND DELETE PROFILE' : 'api/userprofile/update/id',
        'CONFIRM EMAIL':'api/confirm-email/id/',
        'LOGIN':'api/token/',
        'REFRESH_TOKEN': 'api/token/refresh/',
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
    return redirect('https://bmp-inovations.vercel.app/login')


class UserGetUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def users_update(self, serializer):
        instance = serializer.save()

    def users_destroy(self, instance):
        return super().perform_destroy(instance)
    

class UserProfileGet(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated]


class UserProfileGetUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'

    def user_update(self, serializer):
        instance = serializer.save()



class ProductGetCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            return Response({
                'message' : 'Product Created successfully',
                'status' : 'SUCCESS'
                }, status=status.HTTP_201_CREATED)
        
        else:
            return Response({
                'message': 'Product Creation Failed',
                'status' : 'FAILED'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProductDetailsGetUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    # def product_update(self, serializer):
    #     instance = serializer.save()
    #     return instance


    def product_delete(self, instance):
        return super().perform_destroy(instance)