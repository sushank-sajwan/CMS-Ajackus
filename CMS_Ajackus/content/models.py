from django.db import models
from django.db.models import fields
from django.db.models.functions import Lower

# Register Lower Lookup for CharField
fields.CharField.register_lookup(Lower)


class Content(models.Model):
    '''
        - Body is CharField instead of TextField cause we have known word limit.
        - Considering category will be a label.
        - We could have created seprate table for Category but I was not sure about the need of it.
        - file_path is defined to store the path of pdf stored on default_storage(media folder/ s3 bucket).
    '''
    author = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    title = fields.CharField(max_length=30)
    body = fields.CharField(max_length=300)
    summary = fields.CharField(max_length=60)
    file_path = fields.CharField(max_length=512)
    category = fields.CharField(max_length=32, default='')

    REQUIRED_FIELDS = ['title', 'body', 'summary', 'file_path']

    def __str__(self):
        return self.title