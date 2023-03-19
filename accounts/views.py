from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import  SubAdminSerializer
from .models import User
from .permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import logout
from .serializers import MyTokenObtainPairSerializer, UserDetailSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


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