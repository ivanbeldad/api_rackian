import random
import string

from rest_framework import serializers
from rest_framework.reverse import reverse

from storage.models import Folder, File
import mimetypes
import os


def custom_identifier():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))


class FileFieldCustom(serializers.FileField):
    def to_representation(self, value):
        identifier = File.objects.filter(link=value.name).first().id
        url = reverse('download', request=self.context['request'], kwargs={'id': identifier})
        return url


class FolderSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(help_text='', read_only=True)
    link = serializers.SerializerMethodField('download_link', help_text='Zip downloadable', read_only=True)

    class Meta:
        model = Folder
        fields = '__all__'
        read_only_fields = ('user', 'id')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['id'] = user.id + '-' + custom_identifier()
        validated_data['user'] = user
        return Folder.objects.create(**validated_data)

    def download_link(self, folder):
        request = self.context['request']
        absolute_url = request.build_absolute_uri().replace(request.path, '')
        downloadable_url = ''.join((absolute_url, '/v1/download/', folder.id, '/'))
        return downloadable_url


class FileSerializer(serializers.HyperlinkedModelSerializer):
    link = FileFieldCustom(help_text='The binary data itself', required=False)
    id = serializers.CharField(read_only=True)
    mime_type = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('user', 'size',)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['id'] = user.id + '-' + custom_identifier()
        validated_data['user'] = user
        validated_data['name'] = os.path.splitext(validated_data['link'].name)[0]
        try:
            validated_data['extension'] = os.path.splitext(validated_data['link'].name)[1]
        except Exception:
            validated_data['extension'] = ''
        validated_data['size'] = validated_data['link'].size
        try:
            if not validated_data['mime_type']:
                validated_data['mime_type'] = mimetypes.guess_type(validated_data['link'].name)[0]
        except KeyError:
            validated_data['mime_type'] = 'unknown'
        return File.objects.create(**validated_data)


class FileUpdateSerializer(serializers.HyperlinkedModelSerializer):
    link = FileFieldCustom(help_text='The binary data itself', read_only=True)
    id = serializers.CharField(read_only=True)
    mime_type = serializers.CharField(read_only=True)
    name = serializers.CharField(required=False)

    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('user', 'size',)
