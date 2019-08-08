import requests
from rest_framework.test import APITestCase
from rest_framework import status as st
from .tools import jira_connect
from .serializers import BoardsSerializer, ProjectSerializer

DOMAIN = 'http://127.0.0.1:8080'


def send_request(url, method="GET", data=None, permission=''):
    if method == "GET":
        return requests.get(f'{DOMAIN}{url}')

    if method == "POST":
        return requests.post(f'{DOMAIN}{url}', data=data)
    if method == "DELETE":
        return requests.delete(f'{DOMAIN}{url}', data=data)

    if method == "PATCH":
        return requests.patch(f'{DOMAIN}{url}', data=data)


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

