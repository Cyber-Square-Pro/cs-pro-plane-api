from django.urls import path
from api.views import WorkspaceEndpoint

urlpatterns = [
    path('workspace/', WorkspaceEndpoint.as_view({
        'post': 'create'
    }), name='create_workspace'),


]
