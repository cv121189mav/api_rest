from rest_framework import serializers
import maya


class ProjectSerializer(serializers.Serializer):
    project = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    lead = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_description(self, instance):
        return instance.raw['description']

    def get_lead(self, instance):
        return instance.raw['lead']

    def get_id(self, instance):
        return instance.raw['id']

    def get_project(self, instance):
        return instance.raw['name']


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
    summary = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    key = serializers.CharField()
    id = serializers.IntegerField()
    issue_type = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    assignee = serializers.SerializerMethodField()
    timespent = serializers.SerializerMethodField()
    aggregatetimespent = serializers.SerializerMethodField()
    resolutiondate = serializers.SerializerMethodField()

    # trouble with resolution - NoType has no 'name'
    # resolution = serializers.SerializerMethodField()

    labels = serializers.SerializerMethodField()
    subtasks = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    timeestimate = serializers.SerializerMethodField()
    aggregatetimeoriginalestimate = serializers.SerializerMethodField()
    timeoriginalestimate = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_timeestimate(self, instance):
        return instance.fields.timeestimate

    def get_aggregatetimeoriginalestimate(self, instance):
        return instance.fields.aggregatetimeoriginalestimate

    def get_timeoriginalestimate(self, instance):
        return instance.fields.timeoriginalestimate

    def get_status(self, instance):
        return instance.fields.status.name

    # trouble with resolution - NoType has no 'name'
    # def get_resolution(self, instance):
    #     return instance.fields.resolution.name

    def get_priority(self, instance):
        return instance.fields.priority.name

    def get_subtasks(self, instance):
        return len(instance.fields.subtasks)

    def get_labels(self, instance):
        return ', '.join(label for label in instance.fields.labels)

    def get_resolutiondate(self, instance):
        return instance.fields.resolutiondate

    def get_aggregatetimespent(self, instance):
        return instance.fields.aggregatetimespent

    def get_timespent(self, instance):
        return instance.fields.timespent

    def get_assignee(self, instance):
        return instance.fields.assignee.name

    def get_issue_type(self, instance):
        return instance.fields.issuetype.name

    def get_created(self, instance):
        return maya.parse(instance.fields.created).date.isoformat()

    def get_description(self, instance):
        return instance.fields.description

    def get_summary(self, instance):
        return instance.fields.summary


class WorkSheetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
