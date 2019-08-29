from rest_framework.test import APITestCase
from rest_framework import status as st

from api_jira import tools
from .tools import jira_connect
from .serializers import BoardsSerializer, ProjectSerializer, BoardSerializer, IssueSerializer
from .utils import send_request


class ProjectViewTest(APITestCase):

    def test_show_project(self):
        self.test_project = jira_connect.project('BI')
        serializer = ProjectSerializer(self.test_project)

        response = send_request(f'/api/v1/project/{self.test_project.id}/',
                                method="GET")

        self.assertEqual(st.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json(), serializer.data)


class BoardsListTest(APITestCase):

    def test_list_boards(self):
        self.test_list_boards = jira_connect.boards()
        serializer = BoardsSerializer(self.test_list_boards)

        response = send_request(f'/api/v1/boards/',
                                method="GET")

        self.assertEqual(st.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json(), serializer.data)


class BoardDetailTest(APITestCase):

    def test_detail_board(self):
        self.test_board_id = 31
        self.board = jira_connect.board(self.test_board_id)
        serializer = BoardSerializer(self.board)

        response = send_request(f'/api/v1/boards/{self.test_board_id}',
                                method="GET")

        self.assertEqual(st.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json(), serializer.data)


class IssuesListTest(APITestCase):

    def test_list_issues(self):
        self.test_board_id = 31
        self.issues = jira_connect.issues_by_board(self.test_board_id)
        serializer = IssueSerializer(instance=self.issues, many=True)

        response = send_request(f'/api/v1/boards/{self.test_board_id}/issues/',
                                method="GET")

        self.assertEqual(st.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json(), serializer.data)


class IssuesRecordTest(APITestCase):

    def test_list_issues(self):
        self.test_board_id = 31
        self.issues = jira_connect.issues_by_board(self.test_board_id)

        response = send_request(f'/api/v1/boards/{self.test_board_id}/issues/',
                                method="POST")

        self.assertEqual(st.HTTP_200_OK, response.status_code)


class DateFilteredRecordTest(APITestCase):

    def test_filtered_list_issues(self):
        self.date_start = '2019-07-19'
        self.date_end = '2019-07-24'
        self.params = {
            'date-start': self.date_start,
            'date-end': self.date_end
        }
        self.jql = tools.add_to_jql('', 'created>=%s and created<=%s' % (self.date_start, self.date_end))
        self.test_board_id = 31
        self.issues = jira_connect.issues_by_board(self.test_board_id, jql=self.jql)

        response = send_request(f'/api/v1/boards/{self.test_board_id}/issues/',
                                method="POST", params=self.params)

        self.assertEqual(st.HTTP_200_OK, response.status_code)


class TypeFilteredRecordTest(APITestCase):

    def test_filtered_list_issues(self):
        self.issue_type = 'story'
        self.params = {'issue-type': self.issue_type}
        self.jql = tools.add_to_jql('', 'issuetype=%s' % self.issue_type)
        self.test_board_id = 31
        self.issues = jira_connect.issues_by_board(self.test_board_id, jql=self.jql)

        response = send_request(f'/api/v1/boards/{self.test_board_id}/issues/',
                                method="POST", params=self.params)

        self.assertEqual(st.HTTP_200_OK, response.status_code)
