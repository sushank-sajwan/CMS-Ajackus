from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxLengthValidator, MaxValueValidator,
                                    MinLengthValidator, MinValueValidator,
                                    RegexValidator)
from django.db.models import fields


class User(AbstractUser):
    """
    - extended the User model of django to reuse existing user model with few modifications.
    - Phone Number is PositiveBigInt (Positive Integer is not enough) with validation of accepting 10 digits.
    - Pincode is PositiveInt with validation of accept only 6 digits.
    - other feilds are optional only username is required as we are using DjangoUserModel.
    - Added REQUIRED_FIELDS to define required feilds.
    """

    phone_validator = [
            MinValueValidator(7000000000, message='Invalid Phone Number'),
            MaxValueValidator(9999999999, message='Invalid Phone Number')
        ]
    
    pincode_validator = [
            MinValueValidator(100000, message='Invalid Pincode'),
            MaxValueValidator(999999, message='Invalid Pincode')
        ]
    
    full_name_validator = [RegexValidator(
            '^[a-zA-Z]+ [a-zA-Z]+$',
            'Invalid Full Name'
            )]

    USER_TYPE_CHOICES = ( 
        (1, "Admin"),
        (2, "Author")
    ) 
    
    full_name = fields.CharField(max_length=128, validators=  full_name_validator)
    phone = fields.PositiveBigIntegerField(unique=True, validators= phone_validator)
    pincode = fields.PositiveIntegerField(validators=pincode_validator)
    user_type = fields.PositiveIntegerField(choices = USER_TYPE_CHOICES, default=USER_TYPE_CHOICES[0][0])
    address = fields.CharField(max_length=128, default='')
    city = fields.CharField(max_length=32, default='')
    state = fields.CharField(max_length=32, default='')
    country = fields.CharField(max_length=32, default='')

    REQUIRED_FIELDS = ['full_name', 'email', 'phone', 'pincode']

    '''
        - Email Must be unique to be used for login.
    '''

    class Meta(object):
        unique_together = ('email',)

    def __str__(self):
        return self.full_name