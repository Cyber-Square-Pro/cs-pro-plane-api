from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from db.models import User
import uuid
from django.contrib.auth.hashers import make_password
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
        password = email.strip().lower()

        
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
            print(user)
            access_token, refresh_token = get_tokens_for_user(user)
            print(access_token)
            print(refresh_token)
            return Response(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    'statusCode': 201
                },
            )
        return Response(
            {
                'response': 'Email Exists',
                'statusCode': 409
            },
        )
       
    
# class SignInEndPoint(APIView):

