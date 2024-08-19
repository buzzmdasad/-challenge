from rest_framework import serializers
from .models import UserDetails
from rest_framework.authtoken.models import Token
import re
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'

class RecruiterSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UserDetails
        fields = ['name', 'designation', 'company', 'email', 'date_of_birth', 'gender', 'mobile_number', 'about_company', 'website', 'password',]
        error_messages = {
            'email': {
                'invalid': 'Enter a valid email',  # Custom error message
            }
        }
class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
