from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import  SubAdminSerializer, ForgotPasswordSerializer, VerifyCodeSerializer, ResetPasswordSerializer
from .models import User, ForgotPassword, VerifyCode, ResetPassword
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
from django.utils import timezone


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
    
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # generate a verification code and send it to the user's email
        code = random.randint(100000, 999999)
        send_mail(
            'Password Reset Verification Code',
            f'Use the following code to reset your password: {code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        # store the verification code in the database
        forgot_password = ForgotPassword.objects.create(user=user, code=code)
        forgot_password.save()

        return Response({'message': 'Verification code sent to email.'}, status=status.HTTP_200_OK)


    
class VerifyCodeView(APIView):
    def post(self, request):
        code = request.data.get('code')

        try:
            forgot_password = ForgotPassword.objects.get(code=code)
        except ForgotPassword.DoesNotExist:
            return Response({'message': 'Invalid code.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Code verified successfully.', 'user_id': forgot_password.user.id}, status=status.HTTP_200_OK)
    

class ResetPasswordView(APIView):
    def post(self, request):

        user_id = request.data.get('user_id')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password != confirm_password:
            return Response({'message': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(password)
        user.save()

        return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)




    
   
