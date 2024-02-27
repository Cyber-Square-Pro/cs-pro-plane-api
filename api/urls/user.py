from django.urls import path
from api.views import (
    SetPasswordEndpoint, 
    EmailEndPoint, 
    UpdateUserProfileEndpoint,
    EmailVerifyEndPoint
    )

urlpatterns = [
    path('user/password/set/', SetPasswordEndpoint.as_view(), name = 'set_password' ),
    path('user/email/',EmailEndPoint.as_view(), name = 'user_email' ),
    path('user/email/verify',EmailVerifyEndPoint.as_view(), name = 'verify_email' ),

    path('users/me/',UpdateUserProfileEndpoint.as_view(), name = 'user_user' ),
   

]