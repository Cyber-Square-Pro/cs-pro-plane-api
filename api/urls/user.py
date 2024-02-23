from django.urls import path
from api.views import SetPasswordEndpoint

urlpatterns = [
    path('user/password/set/', SetPasswordEndpoint.as_view(), name = 'set_password' )
]