from django.urls import path
from .views import AnalyzeView, DownloadView, TaskStatusView, FileRetrieveView

urlpatterns = [
    path('analyze/', AnalyzeView.as_view(), name='analyze'),
    path('download/', DownloadView.as_view(), name='download'),
    path('status/<str:task_id>/', TaskStatusView.as_view(), name='task_status'),
    path('retrieve/<str:task_id>/', FileRetrieveView.as_view(), name='file_retrieve'),
]
