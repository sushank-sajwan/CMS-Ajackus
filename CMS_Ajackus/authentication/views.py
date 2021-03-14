import csv
import io

from django.http import HttpResponse
from knox import views as knox
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserProfileSerializer
from .services import get_user_instance

# Defined as GLOBAL as we need it at multiple places, we can make it local as well.
HEADER_FORMAT = ['Email*','Password*','Full Name*','Phone*','Address','City','State','Country','Pincode*']

class LoginView(knox.LoginView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Verify User Credential and get user instance.
        request.user = get_user_instance(username, email, password)

        # Logout if already logged in.
        knox.LogoutAllView().post(request, *args, **kwargs)

        # Generate and send knox token.
        return super(LoginView, self).post(request, *args, **kwargs)


'''
    - UserImportTemplate is provieded for user's convenience.
'''
class UserImportTemplateView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):

        # Only Superuser can get the template.
        if not request.user.is_staff:
            raise PermissionDenied
        
        # Write Header and send CSV File as response
        response = HttpResponse(content_type='text/csv')
        csv.writer(response).writerow(HEADER_FORMAT)
        response['Content-Disposition'] = 'attachment; filename="UserImportTemplate"'
        return response


class AdminImportView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        input_file = request.data.get('file')

        # Check if file is CSV or not
        if not input_file.name.endswith('.csv'):
            raise ValidationError('upsupported file format.')
        
        #Get Users count for generating username
        users_count  = User.objects.count() + 1
        
        # Added Decode to avoid errors due to non-unicode charecters entered  by user.
        csv_reader = csv.reader(io.StringIO(input_file.read().decode('utf-8', 'ignore')))
        
        # To Escape First Line
        first_line = True

        created_users = []

        # Create Multiple Users
        for record in csv_reader:

            # Check if Headers are tempered and skip first line
            if first_line:
                if record == HEADER_FORMAT:
                    first_line = False
                    continue
                
                else:
                    raise ValidationError('Invalid File Template')
            
            # Create a username as we are using AbstractUser
            username = record[2].split(' ')[0]+str(users_count)

            '''
                Exception Handling in case anything goes wrong (ex. - wrong data, user exists, validation fail)
                and continue to create other users
            '''

            try:
                instance = User.objects.create_user(
                                username = username,
                                email = record[0],
                                password = record[1],
                                first_name = record[2].split(' ')[0],
                                last_name = record[2].split(' ')[1],
                                full_name = record[2],
                                phone = record[3],
                                address = record[4],
                                city = record[5],
                                state = record[6],
                                country = record[7],
                                pincode = record[8]
                            )

            except IntegrityError:
                continue
            
            created_users.append(instance)

            # to make username unique
            users_count += 1
        
        # Return Created Users
        return Response(self.serializer_class(created_users, many=True).data)


class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserProfileSerializer
    
    def post(self, request, *args, **kwargs):

        # User Count for creating username
        users_count  = User.objects.count()

        # Locally used variables
        full_name = request.data.get('full_name')
        username = full_name.split(' ')[0]+str(users_count + 1)
        address = request.data.get('address')
        city = request.data.get('city')
        state = request.data.get('state')
        country = request.data.get('country')

        # Create Users
        instance = User.objects.create_user(
                        username = username,
                        email = request.data.get('email'),
                        password = request.data.get('password'),
                        first_name = full_name.split(' ')[0],
                        last_name = full_name.split(' ')[1],
                        full_name = full_name,
                        user_type = 1,
                        phone = request.data.get('phone'),
                        address = address if address else '',
                        city = city if city else '',
                        state = city if city else '',
                        country = country if country else '',
                        pincode = request.data.get('pincode')
                    )
        
        # Return Created user's Data
        return Response(self.serializer_class(instance).data)