from django.contrib.auth import authenticate
from django.utils import timezone
from knox.auth import TokenAuthentication
from knox.settings import knox_settings
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from .models import User

'''
    Token Timeout Authentication 
'''
class KnoxTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        try:
            result = super(KnoxTokenAuthentication, self).authenticate(request)
            if result:
                user, auth_token = result
                current_expiry = auth_token.expiry
                new_expiry = timezone.now() + knox_settings.TOKEN_TTL
                auth_token.expires = new_expiry
                if (new_expiry - current_expiry).total_seconds() > 1:
                    pass
            return result
        except AuthenticationFailed:
            return None


def get_user_instance(username, email, password):
    
    '''
        - Verify the user credentials.
        - Logout from running sessions.
    '''

    # Check if user exists else throw error.
    try:
        if username:
            instance = User.objects.get(username=username)
        else:
            instance = User.objects.get(email=email)
    
    except User.DoesNotExist:
        raise ValidationError("User does not exists")
    
    # validate the user credentials.
    if  not authenticate(username=instance.username, password=password):
        raise ValidationError("User/ Password does not match")
    
    return instance


def data_validation(record):
    
    '''
        - Verify the user credentials.
        - Logout from running sessions.
    '''

    # Check if user exists else throw error.
    try:
        if username:
            instance = User.objects.get(username=username)
        else:
            instance = User.objects.get(email=email)
    
    except User.DoesNotExist:
        raise ValidationError("User does not exists")
    
    # validate the user credentials.
    if  not authenticate(username=instance.username, password=password):
        raise ValidationError("User/ Password does not match")
    
    return instance