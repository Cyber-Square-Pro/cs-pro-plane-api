from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from db.models import User
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from api.serializers import UserEmailSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from db.models import VerificationCode
from ..services import generate_verification_code
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
        user = User.objects.get(id = request.user_id)
        verification_code = generate_verification_code()

        user_record = VerificationCode.objects.filter(user = request.user_id).first()
        if not user_record:
            _ = VerificationCode.objects.create(user = user, code = verification_code)
        
        else:
            user_record.code = verification_code
            user_record.created_at = timezone.now()
            user_record.save()
        
        # subject = 'Verification code'
        # recipient_list = [user.email, ]
        # template = get_template('email_template.html')
        # context = {'verification_code': verification_code, 'recipient_email': user.email  }
        # html_content = template.render(context)
        # email = EmailMultiAlternatives(subject, 'Body of the email', 'mohammedrifad17@gmail.com', recipient_list)
        # email.attach_alternative(html_content, 'text/html')
        # email.send()
        token_response = self.handle_token_response(request)
        return Response({
            'message': 'Verification code sent',
            'statusCode': 200,
             **token_response
        })


class EmailVerifyEndPoint(APIView,TokenResponseMixin):
    permission_classes = [CustomJWTPermission]

    def post(self, request):
        code = request.data['code']
        user_record = VerificationCode.objects.get(user = request.user_id)
        token_response = self.handle_token_response(request)
        
        if user_record.code == code:
             

            if not user_record.is_expired():
                user_record.user.is_email_verified = True
                return Response({
                'message': 'Email verified succesfully',
                'statusCode': 200,
                **token_response
            })

            else:
                print('expired')

        
        return Response({
                'message': 'Incorrect code',
                'statusCode': 405,
                **token_response
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
