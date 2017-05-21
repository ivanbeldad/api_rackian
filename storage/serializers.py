from rest_framework import serializers
from rest_framework.reverse import reverse
from storage.models import Folder, File
import mimetypes
import os


class FileFieldCustom(serializers.FileField):
    def to_representation(self, value):
        identifier = File.objects.filter(link=value.name).first().id
        url = reverse('download', request=self.context['request'], kwargs={'id': identifier})
        return url


class FolderSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(help_text='', read_only=True)

    class Meta:
        model = Folder
        fields = '__all__'
        read_only_fields = ('user', 'id')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Folder.objects.create(**validated_data)


class FileSerializer(serializers.HyperlinkedModelSerializer):
    link = FileFieldCustom(help_text='The binary data itself')
    id = serializers.CharField(read_only=True)
    mime_type = serializers.CharField(required=False)

    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('user', 'size', 'name')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['name'] = os.path.splitext(validated_data['link'].name)[0]
        try:
            validated_data['extension'] = os.path.splitext(validated_data['link'].name)[1]
        except Exception:
            validated_data['extension'] = ''
        validated_data['size'] = validated_data['link'].size
        if not validated_data['mime_type']:
            validated_data['mime_type'] = mimetypes.guess_type(validated_data['link'].name)[0]
        return File.objects.create(**validated_data)
