from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token
import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'space', 'last_login')


class TokenSerializer(serializers.Serializer):
    def create(self, validated_data):
        return Token(**validated_data)

    def update(self, instance, validated_data):
        instance.key = validated_data.get('key', instance.key)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.created = validated_data.get('created', instance.created)
        return instance

    key = serializers.CharField()
    user_id = serializers.CharField()
    created = serializers.DateTimeField()
    expires = serializers.SerializerMethodField('calculate_expires')

    def calculate_expires(self, obj):
        expiration = obj.created
        expiration += datetime.timedelta(hours=720)
        return expiration
