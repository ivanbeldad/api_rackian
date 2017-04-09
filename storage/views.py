from rest_framework import viewsets
from storage.models import Folder, File
from storage.serializers import FolderSerializer, FileSerializer
from rest_framework import authentication, permissions


class FolderViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Folders.
    """
    serializer_class = FolderSerializer
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)


class FileViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Files.
    """
    serializer_class = FileSerializer
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)
