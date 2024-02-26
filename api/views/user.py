from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from db.models import User
from django.core.mail import send_mail
from api.serializers import UserEmailSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from api.permissions import CustomJWTPermission
from rest_framework.permissions import IsAuthenticated
from .base import TokenResponseMixin

class SetPasswordEndpoint(APIView):
    def patch(self, request):
        email = 'rifad@cybersquare.org'
        password = request.data['password']
        encrypted_password = make_password(password)
        User.objects.filter(email=email).update(password=encrypted_password)

        return Response({
            'message': 'Password Created',
            'statusCode': 201
        })


class EmailEndPoint(APIView,TokenResponseMixin):

    permission_classes = [CustomJWTPermission]

    def get(self, request):
        requested_user = getattr(request, 'user_id', None)
        print(requested_user,';;;;')
        user_email = User.objects.get(id=requested_user)
        print(user_email)
        serializer = UserEmailSerializer(user_email)
        token_response = self.handle_token_response(request)
        return Response({
            'email': serializer.data['email'],
            'status_code': 200,
            **token_response
        })

    def post(self, request):
        user = getattr(request, 'user_id', None)
        print(user)
        return Response({
            'message': 'Password Created',
            'status_code': 201
        })

class UpdateUserProfileEndpoint(APIView):
    permission_classes = [CustomJWTPermission]
    def patch(self, request):
        try:
            print(request.user_id,'888888888888')
            user = User.objects.get(pk=request.user_id)
        
            user.onboarding_step['profile_complete'] = True
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']

            user.save()
        except: 
            print('error')
        return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
