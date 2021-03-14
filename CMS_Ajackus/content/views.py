from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Content
from .serializers import ContentSerializer
from .services import generate_file_url


# Seperate Views are created for better handling when project become large.
class ContentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContentSerializer
    
    def get(self, request, *args, **kwargs):
        
        # Admin can access any authors data (Requirements) not all.
        # Admin will need to send authors to get data else he will get no data.
        # If required to get all we can send all as well.
        
        author_list = request.query_params.get('author')

        if request.user.user_type == 0 and not author_list:
            raise ValidationError('Please provide the author_id')
            
        # If Admin, send requested authos's content.
        if author_list and request.user.user_type == 0:
            queryset = Content.objects.filter(author__in = author_list.split(','))
        
        # If Author, send his content.
        else:
            queryset = Content.objects.filter(author = request.user)
        
        # Return the details
        return Response(self.serializer_class(queryset, many=True).data)


class ContentCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContentSerializer
    
    def post(self, request, *args, **kwargs):
        
        # Used generate_file_url so we can easily update it in cloud deployment.

        # Admin Cannot Create the Records
        if request.user.user_type == 0:
            raise PermissionDenied
        
        # To Avoid Integrity Error During Object Creation
        category = request.data.get('category')

        # Create Record in DB
        instance = Content.objects.create(
                        author = request.user,
                        title = request.data.get('title'),
                        body = request.data.get('body'),
                        summary = request.data.get('summary'),
                        file_path = generate_file_url(request.user, request.data.get('file')),
                        category = category if category else ''
                    )

        # Return Created Record
        return Response(self.serializer_class(instance).data)


class ContentUpdateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContentSerializer
    
    def put(self, request, *args, **kwargs):

        # Get Object
        instance = Content.objects.get(id = kwargs.get('pk'))

        # Validate if user have access to edit the object
        if request.user.user_type == 1 and request.user != instance.author:
            raise PermissionDenied

        # get requested data
        title = request.data.get('title')
        body = request.data.get('body')
        summary = request.data.get('summary')
        file_object = request.data.get('file')
        category = request.data.get('category')

        # update requested data else not
        if title:
            instance.title = title
        
        if body:
            instance.body = body
        
        if summary:
            instance.summary = summary
        
        if file_object:
            # Remove Existing File from Media Storage
            default_storage.delete(settings.MEDIA_ROOT + '/'+instance.file_path)
            
            # add new file to DB and Storage
            instance.file_object = generate_file_url(instance.author, file_object)
        
        if category:
            instance.category = category

        instance.save()
        return Response(self.serializer_class(instance).data)


class ContentDeleteView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContentSerializer
    
    def delete(self, request, *args, **kwargs):
        # Get Instance.
        instance = Content.objects.get(id = kwargs.get('pk'))

        # Validate if user have access to edit the object
        if request.user.user_type == 1 and request.user != instance.author:
            raise PermissionDenied
        
        # Delete instance
        instance.delete()
        return Response(status=200)

# Seperate SerachView so we can provide complex seraching without making FetchAPI Complex.
class ContentSearchView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContentSerializer
    
    def get(self, request, *args, **kwargs):
        
        # We can improve perfomance if combination search is not required (Single Field Search One Time).
        # If Admin, send requested author's content.
        if request.user.user_type == 0:
            queryset = Content.objects.all()
        
        # If Author, send his content.
        else:
            queryset = Content.objects.filter(author = request.user)
        
        # Get Search Input - Combination is accepted as well.
        title = request.query_params.get('title')
        body = request.query_params.get('body')
        summary = request.query_params.get('summary')
        category = request.query_params.get('category')

        # Apply Search
        # lower is used to avoid case - sensitivity in search.
        if title:
            queryset = queryset.filter(title__lower__icontains = title)
        
        if body:
            queryset = queryset.filter(body__lower__icontains = body)
        
        if summary:
            queryset = queryset.filter(summary__lower__icontains = summary)
        
        if category:
            queryset = queryset.filter(category__lower__icontains = category)

        # Return the details
        return Response(self.serializer_class(queryset, many=True).data)
