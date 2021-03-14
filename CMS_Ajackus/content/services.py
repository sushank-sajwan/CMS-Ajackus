import time

from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.exceptions import ValidationError


def generate_file_url(author, file_object):
    
    # Check file_object is PDF or not
    if not file_object.name.endswith('pdf'):
        raise ValidationError('Invalid File Format')
    
    # Create Custom Path for storage ('/bookstore/<author.id>/')
    default_location = '{}{}/'.format(settings.FILE_PATH, author.id)

    # Final Url for file location
    file_url = default_location + str(time.time()) + '.pdf'

    # Save file to default_storage.
    # Default storage used so we can configure the default storage for cloudfile hosting during deployment.
    default_storage.save(settings.MEDIA_ROOT + '/'+ file_url, file_object)
    
    # return file url
    return file_url