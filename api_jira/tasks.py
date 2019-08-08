from __future__ import absolute_import, unicode_literals
from .celery import app
from . import tools


@app.task
def record_data(issues, tab_sheet_id):
    tools.record_data(issues, tab_sheet_id)
    return 'success'
