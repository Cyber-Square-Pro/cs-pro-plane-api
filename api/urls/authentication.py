from django.urls import path
from api.views import SignUpEndpoint

urlpatterns = [
    path('sign-up/', SignUpEndpoint.as_view(), name = 'sign-up' )
]
