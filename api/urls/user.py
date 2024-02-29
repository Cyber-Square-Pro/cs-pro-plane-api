from django.urls import path
from api.views import (
    SetPasswordEndpoint, 
    EmailEndPoint, 
    UpdateUserProfileEndpoint,
    UserEndPoint,
    EmailVerifyEndPoint,
    UserEndPoint,
    WorkspaceEndPoint,
    UpdateUserOnBoardedEndpoint
    )

urlpatterns = [
    path('user/password/set/', SetPasswordEndpoint.as_view(), name = 'set_password' ),
    path('user/email/',EmailEndPoint.as_view(), name = 'user_email' ),
    path('user/email/verify',EmailVerifyEndPoint.as_view(), name = 'verify_email' ),
    path('users/me/',UserEndPoint.as_view({
        'get': 'retrieve',
        'patch': 'partial_update'
    }), name = 'retrieve_user' ),

 path(
        "users/me/settings/",
        UserEndPoint.as_view(
            {
                "get": "retrieve_user_settings",
            }
        ),
        name="users",
    ),
    path(
        "users/me/workspaces/",
        WorkspaceEndPoint.as_view(),
        name="user-workspace",
    ),
     path(
        "users/me/onboard/",
        UpdateUserOnBoardedEndpoint.as_view(),
        name="user-workspace",
    ),
   

]