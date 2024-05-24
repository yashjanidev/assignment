from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Only include necessary fields


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    user_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True, source='users'
    )
    client = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users',
                  'user_ids', 'created_at', 'created_by']
        read_only_fields = ['client', 'created_by', 'created_at']

    def create(self, validated_data):
        user_ids = validated_data.pop('users')
        project = Project.objects.create(**validated_data)
        project.users.set(user_ids)
        return project


class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        return obj.created_by.username if obj.created_by else None

    class Meta:
        model = Client
        fields = ('id', 'client_name', 'created_at', 'created_by',)


class ClientDetailSerializer(ClientSerializer):
    class Meta:
        model = Client
        fields = ('id', 'client_name', 'projects',
                  'created_at', 'created_by', 'updated_at',)
