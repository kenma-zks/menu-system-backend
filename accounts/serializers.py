from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate


class SubAdminSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'password', 'active']
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validate_data):
        password = validate_data.pop('password', None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
      
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print(user)

        token = super().get_token(user)
        # print(token)

        # Add custom claims
        # token['name'] = user.name
        # ...

        return token

    def validate(self, attrs):
        # Get the user object using the email address
        user = User.objects.get(email=attrs['email'])
        result =(attrs['password'], user.password)
        # check_password method is how authenticate method validates under the hood                
        user = authenticate(
        username_field="email", username=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Incorrect Credentials")
        return super().validate(attrs) 
           
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'active', 'staff', 'admin']


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)