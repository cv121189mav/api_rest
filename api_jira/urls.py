from django.urls import path, include
from api_jira.views import BoardsViewSet, ProjectView, IssuesViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'boards', BoardsViewSet, basename='boards')

urlpatterns = [
    path('project/<str:pk>/', ProjectView.as_view()),
    path('boards/<int:pk>/issues/', IssuesViewSet.as_view(), ),
    path('', include(router.urls)),
]

