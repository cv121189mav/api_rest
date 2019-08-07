from rest_framework import serializers
import maya

class ProjectSerializer(serializers.Serializer):
    project = serializers.CharField()


class BoardSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class BoardsSerializer(serializers.Serializer):
    startAt = serializers.IntegerField()
    isLast = serializers.CharField()
    maxResults = serializers.CharField()
    total = serializers.IntegerField()
    iterable = BoardSerializer(many=True)
    current = serializers.IntegerField()


class IssueSerializer(serializers.Serializer):
    key = serializers.CharField()
    id = serializers.IntegerField()
    issue_type = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    def get_issue_type(self, instance):
        return instance.fields.issuetype.name

    def get_created(self, instance):
        return instance.fields.created
