from rest_framework import serializers
from .models import UserDetails
from rest_framework.authtoken.models import Token
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'

class RecruiterSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UserDetails
        fields = ['name', 'designation', 'company', 'email', 'date_of_birth', 'gender', 'mobile_number', 'about_company', 'website', 'password']

    def validate_name(self, value):
       # Validate name: must contain alphabets and be at least 4 characters long
       if not any(char.isalpha() for char in value):
           raise serializers.ValidationError("Enter a valid name.")
       if len(value) < 4:
           raise serializers.ValidationError("Name must be at least 4 characters long.")
       return value

    def validate_email(self, value):
       # Validate email format
       if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
           raise serializers.ValidationError("Enter a valid email address.")

       # Check for existing email
       if UserDetails.objects.filter(email=value).exists():
           raise serializers.ValidationError("User details with this email already exists.")

       return value

    def validate_mobile_number(self, value):
       # Validate mobile number: must start with 7, 8, or 9 and have exactly 10 characters
       if not (value.startswith(('7', '8', '9')) and len(value) == 10 and value.isdigit()):
           raise serializers.ValidationError("Enter a valid number.")

       # Check for existing mobile number
       if UserDetails.objects.filter(mobile_number=value).exists():
           raise serializers.ValidationError("User details with this mobile number already exists.")

       return value

    def validate_password(self, value):
       # Validate password: must contain uppercase, lowercase, numbers, special characters, and be at least 6 characters long
       if len(value) < 6:
           raise serializers.ValidationError("Password must be at least 6 characters long.")
       if not re.search(r'[A-Z]', value):
           raise serializers.ValidationError("Password must contain at least one uppercase letter.")
       if not re.search(r'[a-z]', value):
           raise serializers.ValidationError("Password must contain at least one lowercase letter.")
       if not re.search(r'\d', value):
           raise serializers.ValidationError("Password must contain at least one number.")
       if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
           raise serializers.ValidationError("Password must contain at least one special character.")
       return value
    def create(self,validated_data):
        """create and return a new User"""
        user = super().create(validated_data)
        return user

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
