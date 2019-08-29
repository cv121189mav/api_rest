from django.http import Http404
from jira import JIRAError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from . import tools
from .serializers import BoardsSerializer, BoardSerializer, IssueSerializer, WorkSheetSerializer, ProjectSerializer
from .tasks import record_data
import datetime
from rest_framework import status as st


class ProjectView(APIView):

    # get project by id
    def get(self, request, pk):
        try:
            project = tools.jira_connect.project(pk)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=st.HTTP_200_OK)
        except Exception as error:
            return Response(error.args.__getitem__(1))


class BoardsViewSet(viewsets.ViewSet):

    # get list of boards
    def list(self, request):
        boards = tools.jira_connect.boards()
        serializer = BoardsSerializer(instance=boards)
        return Response(serializer.data)

    # get detail of board by id
    def retrieve(self, request, pk):
        instance = tools.jira_connect.board(boardKeyOrId=pk)
        # todo jira crutch
        if str(instance.id) != pk:
            raise Http404
        serializer = BoardSerializer(instance=instance)
        return Response(serializer.data)


class IssuesViewSet(APIView):
    jql = ''

    def filters(self):
        self.type_filter()
        self.date_filter()

    def type_filter(self):
        issue_type = self.request.query_params.get('issue-type', None)

        issues_types = tools.get_types_issues()

        if issue_type in issues_types:
            self.jql = tools.add_to_jql(self.jql, 'issuetype=%s' % issue_type)

    def date_filter(self):
        start = self.request.query_params.get('date-start', None)
        end = self.request.query_params.get('date-end', None)

        if end:
            end = datetime.date(int(end.split('-')[0]), int(end.split('-')[1]),
                                int(end.split('-')[2])) + datetime.timedelta(days=1)

        if start is not None:
            self.jql = tools.add_to_jql(self.jql, 'created>=%s' % start)
        if end is not None:
            self.jql = tools.add_to_jql(self.jql, 'created<=%s' % end)

    # get list of issues (filtered or all)
    def get(self, request, pk):
        self.filters()
        try:
            issues = tools.jira_connect.issues_by_board(pk, jql=self.jql)
        except JIRAError as error:
            return Response({'error': error.text, 'type': 'JIRA_ERROR'}, status=error.status_code)
        serializer = IssueSerializer(instance=issues, many=True)
        return Response(serializer.data)

    # record list of issues (filtered or all)
    def post(self, request, pk):
        self.filters()
        try:
            issues = tools.jira_connect.issues_by_board(pk, jql=self.jql)
            serializer = IssueSerializer(instance=issues, many=True)

            # add tab sheet
            tab_sheet = tools.add_tab_sheet(pk)
            serializer_tab_sheet = WorkSheetSerializer(instance=tab_sheet)

            # record data using celery tasks
            record_data.delay(serializer.data, tab_sheet.id)

            # create url of tab sheet
            tab_url = '%s/edit#gid=%d' % (tools.sheet.url, tab_sheet.id)
        except JIRAError as error:
            return Response({'error': error.text, 'type': 'JIRA_ERROR'}, status=error.status_code)

        return Response({'link': tab_url, 'sheet': serializer_tab_sheet.data, 'issues': serializer.data})

