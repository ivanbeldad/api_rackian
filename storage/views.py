import os
import random
import shutil
from zipfile import ZipFile

from django.http import HttpResponse
from rest_framework import authentication, permissions, parsers, status, filters
from rest_framework import viewsets, views
from rest_framework.response import Response

from api_rackian.settings import STORAGE_FOLDER_ABS
from storage.models import Folder, File
from storage.serializers import FolderSerializer, FileSerializer, FileUpdateSerializer


class FolderViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Folders.
    """
    serializer_class = FolderSerializer
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'description', 'parent_folder', 'created_at', 'updated_at',)

    def get_queryset(self):
        folders = Folder.objects.filter(user=self.request.user)
        parent_folder = self.request.query_params.get('parent_folder', None)
        if parent_folder is not None:
            if parent_folder != '':
                folders = folders.filter(parent_folder=parent_folder)
            else:
                folders = folders.filter(parent_folder=None)
        return folders


class FileViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving Files.
    """
    serializer_class = FileSerializer
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'description', 'size', 'mime_type', 'folder', 'created_at', 'updated_at',)

    def get_queryset(self):
        files = File.objects.filter(user=self.request.user)
        folder = self.request.query_params.get('folder', None)
        if folder is not None:
            if folder != '':
                files = files.filter(folder=folder)
            else:
                files = files.filter(folder=None)
        return files

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        try:
            if self.request.method == 'PUT' or self.request.method == 'PATCH':
                serializer_class = FileUpdateSerializer
        except:
            pass

        return serializer_class

    @staticmethod
    def max_space(request):
        # 100MB
        return 104857600

    @staticmethod
    def have_space(request):
        max_space = FileViewSet.max_space(request)
        space = request.user.space
        file_space = request.data['link'].size
        return (space + file_space) <= max_space

    def create(self, request, *args, **kwargs):
        if not FileViewSet.have_space(self.request):
            data = {'error': 'Not enough space'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        user.space = user.space + request.data['link'].size
        user.save()
        return super(FileViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        user.space = user.space - self.get_object().size
        if user.space < 0:
            user.space = 0
        user.save()
        return super(FileViewSet, self).destroy(request, *args, **kwargs)


# class DownloadableResourceView(views.APIView):
#     """
#     A View for download Files.
#     """
#     authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
#
#     def get(self, request, id):
#         """
#         Download file or folder.
#         """
#         real_path = settings.STORAGE_FOLDER_ABS + '/' + id
#
#         try:
#             user = self.request.user
#             file = File.objects.filter(user=user, id=id).first()
#             fp = open(real_path, 'rb')
#             response = HttpResponse(fp.read(), content_type=file.mime_type)
#             response['Content-Length'] = fp.tell()
#             fp.close()
#             if file.extension:
#                 extension = file.extension
#             else:
#                 extension = mimetypes.guess_extension(file.mime_type)
#                 if extension == '.jpe':
#                     extension = '.jpg'
#             response['Content-Disposition'] = 'inline; filename=' + file.name + extension
#         except:
#             return Response('not exists')
#         return response


class DownloadableResourceView(views.APIView):
    """
    A View for download Files.
    """
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)

    def get(self, request, id):
        """
        Download file or folder.
        """
        user = self.request.user

        try:
            file = File.objects.filter(user=user, id=id).first()
            return DownloadableResourceView.download_file(file)
        except:
            pass
        try:
            folder = Folder.objects.filter(user=user, id=id).first()
            return DownloadableResourceView.download_folder(folder)
        except:
            raise
        return Response('not exists')


    @staticmethod
    def download_file(file):
        file_location = ''.join((STORAGE_FOLDER_ABS, '/', file.id))
        fp = open(file_location, 'rb')
        response = HttpResponse(fp.read(), content_type=file.mime_type)
        response['Content-Length'] = fp.tell()
        fp.close()
        response['Content-Disposition'] = 'inline; filename=' + file.name + file.extension
        return response

    @staticmethod
    def download_folder(folder):
        tmp_folder = ''.join(('./tmp-', folder.id, '-', str(random.randint(1000, 9999))))
        root_folder = ''.join((tmp_folder, '/', folder.name))
        os.mkdir(tmp_folder)
        try:
            DownloadableResourceView.generate_folder(tmp_folder, folder)
            shutil.make_archive(root_folder, 'zip', tmp_folder)
            fp = open(''.join((root_folder, '.zip')), 'rb')
            response = HttpResponse(fp.read(), content_type='application/zip')
            response['Content-Length'] = fp.tell()
            fp.close()
            response['Content-Disposition'] = 'inline; filename=' + folder.name + '.zip'
            shutil.rmtree(tmp_folder)
            return response
        except:
            shutil.rmtree(tmp_folder)
            raise

    @staticmethod
    def generate_folder(folder_path, folder):
        if not folder:
            return
        new_folder = ''.join((folder_path, '/', folder.name))
        os.mkdir(new_folder)
        files = File.objects.filter(folder=folder.id).all()
        for file in files:
            file_name = file.name
            origin = ''.join((STORAGE_FOLDER_ABS, '/', file.id))
            dest = ''.join((new_folder, '/', file_name, file.extension))
            number = 1
            while os.path.isfile(dest):
                file_name = ''.join((file.name, ' (', str(number), ')'))
                dest = ''.join((new_folder, '/', file_name, file.extension))
                number += 1
            shutil.copy2(origin, dest)
        folders = Folder.objects.filter(parent_folder=folder.id).all()
        for f in folders:
            DownloadableResourceView.generate_folder(new_folder, f)
