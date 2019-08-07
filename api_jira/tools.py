import pygsheets
from lib.own_jira.client import JIRA

import datetime
from . import views

# connection to jira
options = {'server': 'http://jira.rescrypto.pro/'}
jira_connect = JIRA(options, basic_auth=('oleksandr.mateik', 'Cvdovdmav89'))
# connection to spreadsheets
client = pygsheets.authorize('/test_project/api_jira/credentials.json')
sheet = client.open_by_key("1a5eJDqckUPqrwI0ILMKsyuRInstHArjNo2nqlljV4JE")

# for recording
count_missing_rows = 2

# create jql string
def add_to_jql(jql_str, new_str, type_concat='and'):
    return ' '.join([jql_str, type_concat, new_str]) if jql_str else new_str


def issues_by_board(board_id, jql=None):
    if jql is None:
        jql = jql
    return jira_connect.issues_by_board(board_id, jql=jql)


def type_filter(pk, issue_type):
    jql = ''
    issues_type = ['task', 'story', 'epic', 'bug']
    if issue_type in issues_type:
        jql = add_to_jql(jql, 'issuetype=%s' % issue_type)
        return jira_connect.issues_by_board(pk, jql=jql)


def date_filter(pk, start, end):
    jql = ''
    jql = add_to_jql(jql, 'created>=%s' % start)
    jql = add_to_jql(jql, 'created<=%s' % end)
    return jira_connect.issues_by_board(pk, jql=jql)


def record_data(issues, pk):
    board = jira_connect.board(boardKeyOrId=pk)
    # record name of project
    add_tab_sheet = sheet.add_worksheet(
        '; '.join([board.name, str(datetime.datetime.now())])
    )
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
            'name': 'issuetype',
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
                                      worksheet=add_tab_sheet)
        record_place.value = str(value['name'])

    # set data for each issue
    for count, issue in enumerate(issues):
        for column_index, field in enumerate(fields):
            record_place = pygsheets.Cell(pos=(count_missing_rows + count, column_index + 1),
                                          worksheet=add_tab_sheet)
            value = ''
            if 'created' in field['name']:
                value = issue.fields.created
            if 'assignee' in field['name']:
                value = issue.fields.assignee.name
            elif 'subtasks' in field['name']:
                value = len(issue.fields.subtasks)
            elif 'labels' in field['name']:
                value = ', '.join(label for label in issue.fields.labels)
            else:
                value = getattr(issue.fields, field['name'], field['default'])
            record_place.value = str(value)
