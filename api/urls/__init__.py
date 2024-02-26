from .authentication import urlpatterns as authentication_urls
from .user import urlpatterns as user_urls
from .token import urlpatterns as token_urls
from .workspace import urlpatterns as workspace_url
urlpatterns = [
    *authentication_urls,
    *user_urls,
    *token_urls,
    *workspace_url
]
