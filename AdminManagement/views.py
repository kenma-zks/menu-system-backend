from rest_framework import status
from rest_framework.response import Response
from http.client import ResponseNotReady
from tokenize import Token
from urllib import response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from .serializers import  SubAdminSerializer
from .models import SubAdmin
from .permissions import IsAuthenticated
from datetime import datetime
import jwt, datetime
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework import authentication
from django.contrib.auth import logout

class SubAdminAccountList(generics.ListAPIView):
    serializer_class = SubAdminSerializer
    permission_classes = [IsAuthenticated]
    queryset = SubAdmin.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['admin']

    def get_queryset(self):
        if self.request.user.is_admin:
            return SubAdmin.objects.all()
        return SubAdmin.objects.filter(id=self.request.user.id)

    
class SubAdminAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubAdminSerializer
    permission_classes = [IsAuthenticated]
    queryset = SubAdmin.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.kwargs['pk'])
        if self.request.user.is_admin:
            return obj
        elif obj.id != self.request.user.id:
            raise PermissionDenied(detail="You do not have permission to access this account.")
        return obj


class RegisterView(APIView): 
    def post(self, request):
        serializer = SubAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = SubAdmin.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'user': {
                'email': user.email,
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
            }
        }
        return response  

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = SubAdmin.objects.filter(id=payload['id']).first()
        serializer = SubAdminSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        # your existing code for handling POST requests
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

    def get(self, request):
        # handle GET requests
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)