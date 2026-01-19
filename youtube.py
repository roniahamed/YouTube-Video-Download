import yt_dlp

def get_social_media_video(url):
    ydl_opts = {
    'no_warnings': True,
    'outtmpl': 'downloads/%(id)s.%(ext)s',
    'merge_output_format': 'mp4',
    'format': 'bestvideo+bestaudio/best',
    # 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'quiet': False,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'writethumbnail': False,
    'add_metadata': False,
    }


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print("download Completed")
            return info.get('url')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
# social_media_video_link = "https://www.tiktok.com/@sahalom_howladar/video/7562750709536410887?is_from_webapp=1&sender_device=pc"
social_media_video_link = "https://www.instagram.com/stories/shishirrsiam/"

st = get_social_media_video(social_media_video_link)

print(st)