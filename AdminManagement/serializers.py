from rest_framework import serializers
from .models import SubAdmin

class SubAdminSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'password', 'active']
        model = SubAdmin
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validate_data):
        password = validate_data.pop('password', None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
