from django.conf import settings
from rest_framework import serializers

from .models import Content


class ContentSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the content data
    """
    file_url = serializers.SerializerMethodField()
    
    def get_file_url(self, instance):

        # write logic here to send the generated presigned_url for file on cloud_storage
        return settings.API_BASE + 'content' + settings.MEDIA_URL + instance.file_path

    class Meta:
        model = Content
        fields = ('id', "title", 'body', 'summary', 'file_url', 'category')
