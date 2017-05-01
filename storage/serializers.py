from rest_framework import serializers
from rest_framework.reverse import reverse
from storage.models import Folder, File
import mimetypes


class FileFieldCustom(serializers.FileField):
    def to_representation(self, value):
        identifier = File.objects.filter(link=value.name).first().id
        url = reverse('download', request=self.context['request'], kwargs={'id': identifier})
        return url


class FolderSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField()

    class Meta:
        model = Folder
        fields = '__all__'
        read_only_fields = ('user', 'identifier')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Folder.objects.create(**validated_data)


class FileSerializer(serializers.HyperlinkedModelSerializer):
    link = FileFieldCustom()
    id = serializers.CharField()

    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('user', 'mime_type', 'size')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['size'] = validated_data['link'].size
        validated_data['mime_type'] = mimetypes.guess_type(validated_data['link'].name)[0]
        return File.objects.create(**validated_data)
