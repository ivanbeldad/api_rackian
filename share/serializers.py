from rest_framework import serializers
from rest_framework.reverse import reverse
from . import models
import random
import string


def custom_identifier():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Permission
        fields = '__all__'
        read_only_fields = ('id',)


class FileLinkCustom(serializers.FileField):
    def to_representation(self, value):
        identifier = models.FileLink.objects.filter(link=value).first().id
        url = reverse('share-file', request=self.context['request'], kwargs={'id': identifier})
        return url


class FolderLinkCustom(serializers.FileField):
    def to_representation(self, value):
        identifier = models.FolderLink.objects.filter(link=value).first().id
        url = reverse('share-folder', request=self.context['request'], kwargs={'id': identifier})
        return url


class FileLinkSerializer(serializers.HyperlinkedModelSerializer):
    link = FileLinkCustom('link', help_text='Downloadable')

    class Meta:
        model = models.FileLink
        fields = '__all__'
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['id'] = user.id + '-' + custom_identifier()
        validated_data['link'] = validated_data['id']
        return models.FileLink.objects.create(**validated_data)


class FolderLinkSerializer(serializers.HyperlinkedModelSerializer):
    link = FolderLinkCustom('link', help_text='Downloadable')

    class Meta:
        model = models.FolderLink
        fields = '__all__'
        read_only = ('id',)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['id'] = user.id + '-' + custom_identifier()
        return models.FolderLink.objects.create(**validated_data)
