from celery import shared_task
from .services import VideoDownloaderService
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def download_video_task(self, url, format_id):
    """
    Async task to download video.
    Returns dictionary with file_path and temp_dir to be used by the retrieve view.
    """
    try:
        service = VideoDownloaderService()
        file_path, temp_dir = service.download(url, format_id)
        
        # We return the paths as strings. 
        # Note: In a diverse worker env, workers and web must share the filesystem.
        # Since this is a simple setup on one machine (or mounted volume), this is fine.
        return {
            'file_path': str(file_path),
            'temp_dir': str(temp_dir)
        }
    except Exception as e:
        logger.error(f"Task failed: {e}")
        # Re-raise so Celery marks it as FAILED
        raise e
