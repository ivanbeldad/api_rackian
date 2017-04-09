from rest_framework import viewsets
from django.contrib.auth.models import User
from authentication.serializers import UserSerializer
from rest_framework import authentication, permissions


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Users.
    """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()
