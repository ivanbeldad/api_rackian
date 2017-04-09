from rest_framework import serializers
from storage.models import Folder, File


class FolderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'
        read_only_fields = ('path', 'user')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['path'] = user.username + '/'
        if validated_data['parent_folder']:
            validated_data['path'] += validated_data['parent_folder'].name + '/'
        validated_data['path'] += validated_data['name']
        return Folder.objects.create(**validated_data)

    def validate(self, data):
        """
        Check that the path is not duplicated.
        """
        try:
            Folder.objects.get(user=self.context['request'].user, parent_folder=data['parent_folder'], name=data['name'])
        except Folder.DoesNotExist:
            return data
        raise serializers.ValidationError({'path': 'Duplicated path not allowed.'})


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('path',)
