from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from db.models import User
import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return (
        str(refresh.access_token),
        str(refresh),
    )

class SignUpEndpoint(APIView):
    def post(self, request):

        email = request.data['email']
        password = request.data['password']

        
         # Check if the user already exists
        user = User.objects.filter(email = email)

        if not user.exists():
            encryped_password = make_password(password)
            user = User.objects.create(email = email, password = encryped_password, username= uuid.uuid4().hex)
            user.last_active = timezone.now()
            user.last_login_time = timezone.now()
            user.last_login_ip = request.META.get("REMOTE_ADDR")
            user.last_login_uagent = request.META.get("HTTP_USER_AGENT")
            user.token_updated_at = timezone.now()
            user.last_login = timezone.now()
            user.save()
            
            access_token, refresh_token = get_tokens_for_user(user)
             
            return Response(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    'status_code': 201
                },
            )
        return Response(
            {
                'message': 'Email Exists',
                'status_code': 409
            },
        )
       
    
class SignInEndPoint(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        
        if user is None:
            return Response(
                {
                    'message': 'Sorry, user not found. Please try again.',
                    'status_code':  404
                },
                 
            )
        if not check_password(password, user.password):
             
            return Response(
                {
                    'message': 'Password Incorrect',
                    'status_code':  405
                },
                 
            )

        user.last_active = timezone.now()
        user.last_login_time = timezone.now()
        user.last_login_ip = request.META.get("REMOTE_ADDR")
        user.last_login_uagent = request.META.get("HTTP_USER_AGENT")
        user.token_updated_at = timezone.now()
        user.save()

        access_token, refresh_token = get_tokens_for_user(user)
        is_email_verified = user.is_email_verified
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'status_code': 200,
            'is_email_verified': is_email_verified
        }
        
        return Response(data)

