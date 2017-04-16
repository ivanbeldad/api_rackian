from rest_framework import viewsets
from authentication.serializers import UserSerializer
from rest_framework import authentication, permissions
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Users.
    """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()
