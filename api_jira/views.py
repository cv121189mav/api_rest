from django.http import Http404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from . import tools
from .serializers import BoardsSerializer, BoardSerializer, IssueSerializer


class ProjectView(APIView):

    def get(self, request, pk):
        project = tools.jira_connect.project(pk)
        return Response(data=project.raw)


class BoardsViewSet(viewsets.ViewSet):

    def list(self, request):
        boards = tools.jira_connect.boards()
        serializer = BoardsSerializer(instance=boards)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        instance = tools.jira_connect.board(boardKeyOrId=pk)
        # todo jira crutch
        if str(instance.id) != pk:
            raise Http404
        serializer = BoardSerializer(instance=instance)
        return Response(serializer.data)


class IssuesViewSet(APIView):

    def get(self, request, pk):
        issue_type = request.query_params.get('issue-type', None)
        start = request.query_params.get('start-from', None)
        end = request.query_params.get('end-to', None)
        issues = tools.jira_connect.issues_by_board(pk)

        if issue_type:
            issues = tools.type_filter(pk, issue_type)

        elif start or end:
            issues = tools.date_filter(pk, start, end)

        serializer = IssueSerializer(instance=issues, many=True)

        return Response(serializer.data)

    def post(self, request, pk):

        issue_type = request.query_params.get('issue-type', None)

        start = request.query_params.get('start-from', None)
        end = request.query_params.get('end-to', None)

        issues = tools.jira_connect.issues_by_board(pk)

        if issue_type:
            issues = tools.type_filter(pk, issue_type)

        elif start or end:
            issues = tools.date_filter(pk, start, end)

        tools.record_data(issues, pk)
        return Response({'status': 'recorded'})
