

from .models import UserDetails
from rest_framework.authtoken.models import Token
from rest_framework import serializers
import re
from django.contrib.auth import (authenticate,get_user_model,)
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext as _
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserDetails
#         fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =UserDetails
        fields = ['name', 'designation', 'company', 'email', 'date_of_birth', 'gender', 'mobile_number', 'about_company', 'website', 'password','course','specialization','course_type','college','percentage','year_of_passing','skills','summary','experience_level','designation','responsibilities','company','location','worked_from','to']
        error_messages = {
            'email': {
                'invalid': 'Enter a valid email',  # Custom error message
            }
        }
        extra_kwargs = {
            'email': {
                'validators': [

                    UniqueValidator(
                       queryset=UserDetails.objects.all(),
                       message="user details with this email already exists."
                    )
                ]
            },'mobile_number': {
                'validators': [

                    UniqueValidator(
                       queryset=UserDetails.objects.all(),
                       message="user details with this mobile number already exists."
                    )
                ]
            },
            'password':{'write_only':True},
        }
    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError('Enter a valid email')
        return value

    def validate_name(self, value):
        if not value.isalpha() or len(value) < 4:
            raise serializers.ValidationError('Enter a valid name')
        return value

    def validate_mobile_number(self, value):
        value_str = str(value)
        if not re.match(r'^[789]\d{9}$', value_str):
            raise serializers.ValidationError('Enter a valid number')
        return value

    def validate_password(self,value):
        if len(value)<5:
            message:'Enter a valid password'
            raise ValidationError(message,code='invalid')
        return value
    def create(self,validated_data):
        """craete an return a user"""
        email = validated_data.get('email')
        password = validated_data.pop('password', None)
        user = UserDetails(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        return user
    def update(self,instance,validated_data):
        """Update and return user"""
        password=validated_data.pop('password',None)
        user=super().update(instance,validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Remove keys with None values
        return {key: value for key, value in representation.items() if value is not None}

        #return UserDetails.objects.create_user(self,email, password, **validated_data)
class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                msg = ('Unable to authenticate with provided credentials')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
