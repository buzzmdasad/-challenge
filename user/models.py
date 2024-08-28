from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from user.validators import UserDetailsValidator
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        #email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_admin(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        #extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class UserDetails(AbstractBaseUser):

    email = models.CharField(max_length=255,unique=True,validators=[UserDetailsValidator.validate_email])
    name = models.CharField(max_length=255, validators=[UserDetailsValidator.validate_name])
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10,null=True, blank=True)
    mobile_number = models.IntegerField(validators=[UserDetailsValidator.validate_phone_number])
    address = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=255,validators=[UserDetailsValidator.validate_password])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    course = models.CharField(max_length=255,null=True, blank=True)
    specialization = models.CharField(max_length=255,null=True, blank=True)
    course_type = models.CharField(max_length=255,null=True, blank=True)
    college = models.CharField(max_length=255,null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    year_of_passing = models.IntegerField(null=True, blank=True)
    skills = models.CharField(max_length=255,null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    experience_level = models.CharField(max_length=255,null=True, blank=True)
    designation = models.CharField(max_length=255,null=True, blank=True)
    responsibilities = models.CharField(max_length=255,null=True, blank=True)
    company = models.CharField(max_length=255,null=True, blank=True)
    location = models.CharField(max_length=255,null=True, blank=True)
    worked_from = models.DateField(null=True, blank=True,default=None)
    to = models.DateField(null=True, blank=True,default=None)
    about_company = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
