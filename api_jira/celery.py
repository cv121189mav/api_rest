from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

app = Celery('api_jira',
             broker='pyamqp://guest@localhost//',
             backend='amqp://',
             include=['api_jira.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
