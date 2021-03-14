from rest_framework import serializers

from .models import User


class KnoxUserSerializer(serializers.ModelSerializer):
    """
    This serializer is called by knox directly for user login serialization.
    """
    
    class Meta:
        model = User
        fields = ('id', "username", 'email')


class UserProfileSerializer(serializers.ModelSerializer):

    '''
    This Serializer to send back the user profile data.
    '''

    class Meta:
        model = User
        fields = (
            'id', 
            "username", 
            "first_name", 
            "last_name", 
            "full_name", 
            "phone", 
            "email",
            'pincode',
            'address',
            'city',
            'state',
            'country'
        )