from django.urls import path
from api.views import SignUpEndpoint, SignInEndPoint

urlpatterns = [
    path('user/sign-up/', SignUpEndpoint.as_view(), name = 'sign_up' ),
    path('user/sign-in/', SignInEndPoint.as_view(), name = 'sign_in' )

]
