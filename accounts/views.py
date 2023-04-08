from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import  SubAdminSerializer, ForgotPasswordSerializer
from .models import User, ForgotPassword
from .permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import logout
from .serializers import MyTokenObtainPairSerializer, UserDetailSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
import random
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

class UserAccountList(generics.ListAPIView):
    serializer_class = SubAdminSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['admin']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return User.objects.all()
            return User.objects.filter(id=self.request.user.id)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'pk'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView): 
    def post(self, request):
        serializer = SubAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LogoutView(APIView):

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK, data={"message": "You have been logged out."})
    
@api_view(['POST'])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']


    user = User.objects.get(email=email)
    if user:
        code = random.randint(100000, 999999)
        ForgotPassword.objects.create(user=user)
        send_mail(
            'Forgot Password',
            f'Your code is {code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        print(code)
        return Response(status=status.HTTP_200_OK, data={"message": "Code sent to your email"})
    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "User not found"})


         
    
   
