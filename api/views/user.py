from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from db.models import User
from django.utils import timezone
from rest_framework import viewsets
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from api.serializers import UserEmailSerializer, UserMeSerializer,UserMeSettingsSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from db.models import VerificationCode
from api.serializers import UserSerializer
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


class EmailEndPoint(APIView, TokenResponseMixin):

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
        try:
            user = User.objects.get(id=request.user_id)
            verification_code = generate_verification_code()
            print(user)
            user_record = VerificationCode.objects.filter(
                user=request.user_id).first()
            if not user_record:
                _ = VerificationCode.objects.create(
                    user=user, code=verification_code)

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
            print('tokenre', token_response)
            return Response({
                'message': 'Verification code sent',
                'status_code': 200,
                **token_response
            })
        except Exception as e:
            print(e)


class EmailVerifyEndPoint(APIView, TokenResponseMixin):
    permission_classes = [CustomJWTPermission]

    def post(self, request):

        code = request.data['code']
        user_record = VerificationCode.objects.get(user=request.user_id)
        token_response = self.handle_token_response(request)

        if user_record.code == code:
            user = User.objects.get(id=request.user_id)
            user.onboarding_step['email_verified'] = True
            user.save()
            onboarding_step = user_record.user.onboarding_step
            print(onboarding_step)
            user_record.created_at = timezone.now()
            onboarding_step['email_verified'] = True
            user_record.save()

            return Response({
                'message': 'Email verified succesfully',
                'status_code': 200,
                **token_response
            })
            

        return Response({
            'message': 'Incorrect code',
            'status_code': 405,
            **token_response
        })


class UserEndPoint(viewsets.ViewSet, TokenResponseMixin):
    permission_classes = [CustomJWTPermission]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user_id
    
    def retrieve(self, request):
        user = User.objects.get(id=request.user_id)
        serializer = UserMeSerializer(user)
        return Response(serializer.data)

    def retrieve_user_settings(self, request):
        user = User.objects.get(id = request.user_id)
        serialized_data = UserMeSettingsSerializer(user).data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
    def partial_update(self, request):
        user = User.objects.get(id=request.user_id)
        serializer = UserMeSerializer(
            instance=user, data=request.data,  partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                print(e)

        return Response(serializer.data)


class UpdateUserProfileEndpoint(APIView, TokenResponseMixin):
    permission_classes = [CustomJWTPermission]

    def patch(self, request):
        try:

            user = User.objects.get(pk=request.user_id)

            user.onboarding_step['profile_complete'] = True
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']

            user.save()
        except:
            print('error')
        return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)


class UpdateUserOnBoardedEndpoint(APIView, TokenResponseMixin):
    permission_classes = [CustomJWTPermission]
    def patch(self, request):
        user = User.objects.get(pk=request.user_id)
        user.is_onboarded = request.data.get("is_onboarded", False)
        user.save()
        return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
