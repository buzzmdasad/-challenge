from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re



class UserDetailsValidator:

    @staticmethod
    def validate_name(value):
        if not value.isalpha() or len(value) < 4:
            #message='Enter a valid name'
            raise ValidationError(
                _('Enter a valid name'), code='invalid'
            )
    @staticmethod
    def validate_password(value):
        if len(value)<5:
            #message:'Enter a valid password'
            raise ValidationError(_
                ('Enter a valid password'), code='invalid'
            )


    @staticmethod
    def validate_email(value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValidationError(
                _('Enter a valid email'), code='invalid'
            )
        # if UserDetails.objects.filter(email=value).exists():
        #     raise ValidationError(
        #         _('User details with this email already exists.'), code='invalid'
        #     )

    @staticmethod
    def validate_phone_number(value):
        if not re.match(r'^[789]\d{9}$', value):
             raise ValidationError(
                _('Enter a valid number'), code='invalid'
            )
        # if UserDetails.objects.filter(mobile_number=value).exists():
        #     raise ValidationError(
        #        _('User details with this mobile already exists.'), code='invalid'
        #    )
