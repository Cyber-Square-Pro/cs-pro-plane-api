from django.urls import path
from api.views import SetPasswordEndpoint, EmailEndPoint, UpdateUserProfileEndpoint

urlpatterns = [
    path('user/password/set/', SetPasswordEndpoint.as_view(), name = 'set_password' ),
    path('user/email/',EmailEndPoint.as_view(), name = 'user_email' ),
    path('users/me/',UpdateUserProfileEndpoint.as_view(), name = 'user_user' ),
   

]