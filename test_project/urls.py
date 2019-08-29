from django.contrib import admin
from django.urls import path, include

# from api_jira.views import ProjectView, BoardsViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api_jira.urls')),
    path('chat/', include('chat_aplic.urls'))
]
