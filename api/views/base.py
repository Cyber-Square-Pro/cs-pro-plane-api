from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter

class TokenResponseMixin:
    def handle_token_response(self, request):
        if hasattr(request, 'new_access_token') and hasattr(request, 'new_refresh_token'):
            new_access_token = request.new_access_token
            new_refresh_token = request.new_refresh_token
            print(new_access_token, new_refresh_token)
            return {'access_token': new_access_token, 'refresh_token': new_refresh_token}
        return {}
 

class BaseAPIView(APIView):

    

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )

    filterset_fields = []

    search_fields = []

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
