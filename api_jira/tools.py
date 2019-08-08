import pygsheets
from lib.own_jira.client import JIRA

import datetime

# connection to jira
options = {'server': 'http://jira.rescrypto.pro/'}
jira_connect = JIRA(options, basic_auth=('oleksandr.mateik', 'Cvdovdmav89'))
# connection to spreadsheets
client = pygsheets.authorize('/test_project/api_jira/credentials.json')
sheet = client.open_by_key("1a5eJDqckUPqrwI0ILMKsyuRInstHArjNo2nqlljV4JE")

# variable for recording
count_missing_rows = 2


# create jql string
def add_to_jql(jql_str, new_str, type_concat='and'):
    return ' '.join([jql_str, type_concat, new_str]) if jql_str else new_str


# get issues by board
def issues_by_board(board_id, jql=None):
    if jql is None:
        jql = jql
    return jira_connect.issues_by_board(board_id, jql=jql)


def add_tab_sheet(boardKeyOrId):
    board = jira_connect.board(boardKeyOrId=boardKeyOrId)
    # record name of project
    return sheet.add_worksheet(
        '; '.join([board.name, str(datetime.datetime.now())])
    )


def get_types_issues():
    types_issues = jira_connect.issue_types()
    list_types = list([i.name.lower() for i in types_issues])
    return list_types


def record_data(issues, tab_sheet_id):
    tab_sheet = sheet.worksheet(property='id', value=tab_sheet_id)
    fields = [
        {
            'name': 'created',
            'default': 'noname',
        },
        {
            'name': 'summary',
            'default': 'noname',
        },
        {
            'name': 'priority',
            'default': 'noname',
        },
        {
            'name': 'issue_type',
            'default': 'noname',
        },
        {
            'name': 'description',
            'default': 'noname',
        },
        {
            'name': 'assignee',
            'default': 'noname',
        },
        {
            'name': 'timespent',
            'default': 'noname',
        },
        {
            'name': 'aggregatetimespent',
            'default': 'noname',
        },
        {
            'name': 'resolution',
            'default': 'noname',
        },
        {
            'name': 'resolutiondate',
            'default': 'noname',
        },
        {
            'name': 'labels',
            'default': 'noname',
        },
        {
            'name': 'timeestimate',
            'default': 'noname',
        },
        {
            'name': 'aggregatetimeoriginalestimate',
            'default': 'noname',
        },
        {
            'name': 'timeoriginalestimate',
            'default': 'noname',
        },
        {
            'name': 'status',
            'default': 'noname',
        },
        {
            'name': 'subtasks',
            'default': 'noname',
        },
    ]

    # set headers for each column
    for column_index, value in enumerate(fields):
        record_place = pygsheets.Cell(pos=(1, 1 + column_index),
                                      worksheet=tab_sheet)
        record_place.value = str(value['name'])

    # set data for each issue
    for count, issue in enumerate(issues):
        for column_index, field in enumerate(fields):
            record_place = pygsheets.Cell(pos=(count_missing_rows + count, column_index + 1),
                                          worksheet=tab_sheet)
            value = ''
            value = issue.get(field['name'], field['default'])
            record_place.value = str(value)
