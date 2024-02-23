from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from db.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status


class SetPasswordEndpoint(APIView):
    def patch(self, request):
        email = 'rifad@cybersquare.org'
        password = request.data['password']
        # user = User.objects.get(pk=request.user.id)
        encrypted_password = make_password(password)
        User.objects.filter(email=email).update(password = encrypted_password)

        # user.is_onboarded = request.data.get("is_onboarded", False)
        # user.save()
        return Response({
            'message': 'Password Created',
            'statusCode': 201
        })
