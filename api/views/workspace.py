from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from db.models import User,Workspace, WorkspaceMember
from django.core.mail import send_mail
from api.serializers import UserEmailSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from api.permissions import CustomJWTPermission
from rest_framework.permissions import IsAuthenticated
from .base import TokenResponseMixin
from api.serializers import WorkSpaceSerializer
from rest_framework import viewsets

class WorkspaceEndpoint(viewsets.ViewSet, TokenResponseMixin):
    permission_classes = [ CustomJWTPermission]
    def create(self, request):
        try:
            
            slug = request.data['slug']
            workspace_name = request.data['name']
            organization_size = request.data['organization_size']
            serializer = WorkSpaceSerializer(data=request.data)
            workspace_slug = Workspace.objects.filter(slug = slug).exists()
            if workspace_slug:
                return Response(
                    {'status_code': 409, 
                     'message': 'Workspace URL is already taken!'
                     }) 
            print('first')
            if not workspace_name or not slug:
                return Response(
                    {'message': "Both name and slug are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            print('second')
            if len(workspace_name) > 80 or len(slug) > 48:
                return Response(
                    {'message': "The maximum length for name is 80 and for slug is 48"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            print('third')
            if serializer.is_valid():
                serializer.save(owner_id = request.user_id)
                _ = WorkspaceMember.objects.create(
                    workspace_id=serializer.data["id"],
                    member_id=request.user_id,
                    role=20,
                    
                )
                print('here')
                return Response({
                    'data':serializer.data,
                    'message': 'Workspace Created Succesfully'
                    })
            else:
                print(serializer.errors)
        except Exception as e:
            print(e,'000000000000000')
            None
