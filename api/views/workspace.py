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
from .base import BaseAPIView, TokenResponseMixin
from api.serializers import WorkSpaceSerializer
from rest_framework import viewsets
from django.db.models import (
    Prefetch,
    OuterRef,
    Func,
    F,
    Q,
    Count,
    Case,
    Value,
    CharField,
    When,
    Max,
    IntegerField,
)
class WorkspaceEndpoint(viewsets.ViewSet, BaseAPIView, TokenResponseMixin):
    permission_classes = [ CustomJWTPermission]

    def fetch_workspace(self, request):
        member_count = (
            WorkspaceMember.objects.filter(
                workspace=OuterRef("id"), member__is_bot=False
            )
            .order_by()
            .annotate(count=Func(F("id"), function="Count"))
            .values("count")
        )
        workspace = (
            (
                Workspace.objects.prefetch_related(
                    Prefetch("workspace_member", queryset=WorkspaceMember.objects.all())
                )
                .filter(
                    workspace_member__member=request.user_id,
                )
                .select_related("owner")
            )
            .annotate(total_members=member_count)
            
        )
        token_response = self.handle_token_response(request)

        serializer = WorkSpaceSerializer(self.filter_queryset(workspace), many=True)
        print(serializer.data)
        return Response({
            'data':serializer.data, **token_response})
    
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
             
            if not workspace_name or not slug:
                return Response(
                    {'message': "Both name and slug are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if len(workspace_name) > 80 or len(slug) > 48:
                return Response(
                    {'message': "The maximum length for name is 80 and for slug is 48"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if serializer.is_valid():
                serializer.save(owner_id = request.user_id)
                _ = WorkspaceMember.objects.create(
                    workspace_id=serializer.data["id"],
                    member_id=request.user_id,
                    role=20,
                    
                )
                
                user = User.objects.get(id = request.user_id)
                user.is_onboarded = True
                # user.last_workspace_id = user_workspace.id
                # user.onboarding_step['workspace_create'] = True
                user.save()

                token_response = self.handle_token_response(request)
                return Response({
                    'data':serializer.data,
                    'message': 'Workspace Created Succesfully',
                    **token_response
                    })
            else:
                print(serializer.errors)
        except Exception as e:
            None

 

    
    
class WorkSpaceAvailabilityCheckEndpoint(BaseAPIView,TokenResponseMixin):
    permission_classes = [ CustomJWTPermission]

    def get(self, request):
        slug = request.GET.get("slug", False)

        if not slug or slug == "":
            return Response({
                'message': 'Workspace Slug is required',
                'status_code': 400
                })
        
        workspace = Workspace.objects.filter(slug=slug).exists()
        return Response({
            'status':not workspace,
            'status_code': 200
             })

        
