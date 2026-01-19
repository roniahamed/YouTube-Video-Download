import yt_dlp

def download_best_tiktok(url):
    ydl_opts = {
        'format': 'best[height>=1280]/best[height>=1024]/best',
        
        'outtmpl': 'downloads/%(id)s_%(height)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
     
            return info.get('url')
            
    except Exception as e:

        return None

link = "https://www.tiktok.com/@sahalom_howladar/video/7562750709536410887?is_from_webapp=1&sender_device=pc"
download_best_tiktok(link)