from rest_framework import viewsets, views, authentication, permissions
from rest_framework.authtoken.models import Token
from authentication.serializers import UserSerializer, TokenSerializer
from rest_framework.response import Response
from .models import User
from django.utils import timezone
import datetime


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Users.
    """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()


class TokenView(views.APIView):
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        Get a valid token for one user
        """
        user = self.request.user
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=self.request.user)
        serializer = TokenSerializer(token)
        now = timezone.now()
        expires = TokenView.calculate_expires(serializer.instance.created)
        if now < expires:
            return Response(serializer.data)
        token.delete()
        token = Token.objects.create(user=self.request.user)
        serializer = TokenSerializer(token)
        return Response(serializer.data)

    @staticmethod
    def calculate_expires(created):
        expiration = created
        expiration += datetime.timedelta(hours=720)
        return expiration
