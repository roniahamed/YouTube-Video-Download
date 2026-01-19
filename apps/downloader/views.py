from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from celery.result import AsyncResult
from .services import VideoDownloaderService
from .serializers import AnalyzeSerializer, DownloadSerializer
from .utils import FileCleanupWrapper
from .tasks import download_video_task
import os
import logging

logger = logging.getLogger(__name__)

class AnalyzeView(APIView):
    def post(self, request):
        serializer = AnalyzeSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            service = VideoDownloaderService()
            try:
                data = service.analyze(url)
                return Response(data, status=status.HTTP_200_OK)
            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg:
                    return Response({"error": "Too many requests to video provider"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
                if "403" in err_msg or "Private" in err_msg:
                     return Response({"error": "Content is private or rectricted"}, status=status.HTTP_403_FORBIDDEN)
                
                logger.error(f"Analysis Error: {e}")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DownloadView(APIView):
    def post(self, request):
        """
        Initiates the download task and returns a Task ID.
        """
        serializer = DownloadSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            format_id = serializer.validated_data['format_id']
            
            # Dispatch Async Task
            task = download_video_task.delay(url, format_id)
            
            return Response({
                "task_id": task.id,
                "status": "processing",
                "message": "Download started successfully. Poll /api/v1/status/<task_id>/ for updates."
            }, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskStatusView(APIView):
    def get(self, request, task_id):
        """
        Check the status of a download task.
        """
        result = AsyncResult(task_id)
        
        response_data = {
            "task_id": task_id,
            "status": result.state,
        }

        if result.state == 'SUCCESS':
            # Construct the retrieve URL
            # In a real app, use reverse(). For now, simple string construction.
            # We assume the client knows where to go, or we provide the link.
            response_data['download_url'] = f"/api/v1/retrieve/{task_id}/"
        elif result.state == 'FAILURE':
            response_data['error'] = str(result.result)

        return Response(response_data)

class FileRetrieveView(APIView):
    def get(self, request, task_id):
        """
        Retrieve the downloaded file (once task is SUCCESS).
        """
        result = AsyncResult(task_id)
        
        if result.state != 'SUCCESS':
            return Response({"error": "Task not ready or failed"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Result is the dict we returned in tasks.py
        data = result.result
        file_path = data.get('file_path')
        temp_dir = data.get('temp_dir')
        
        if not file_path or not os.path.exists(file_path):
             return Response({"error": "File expired or not found"}, status=status.HTTP_404_NOT_FOUND)

        filename = os.path.basename(file_path)
        
        # Cleanup Wrapper will delete the file/folder after streaming
        try:
            file_handle = FileCleanupWrapper(file_path, temp_dir)
            response = FileResponse(file_handle, as_attachment=True, filename=filename)
            response['Content-Length'] = os.path.getsize(file_path)
            
            # Optional: We might want to forget the task result now to save Redis memory, 
            # but default expiry is usually fine.
            # result.forget() 
            
            return response
        except Exception as e:
            logger.error(f"Retrieve Error: {e}")
            return Response({"error": "Error retrieving file"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
