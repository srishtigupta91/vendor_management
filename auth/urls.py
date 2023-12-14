# urls.py

from django.urls import path
from .views import ObtainAuthTokenView, CustomAuthToken, UserCreateAPIView

urlpatterns = [
    path('users/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('api-token-auth/', ObtainAuthTokenView.as_view(), name='api_token_auth'),
    path('custom-token-auth/', CustomAuthToken.as_view(), name='custom_token_auth'),
]