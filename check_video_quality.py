import yt_dlp

def check_formats(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
        print("-" * 40)
        print(f"{'Format ID':<15} | {'Resolution':<10} | {'Note'}")
        print("-" * 40)
        
        for f in info['formats']:
            if f.get('vcodec') != 'none':
                res = f"{f.get('height')}p" if f.get('height') else "Unknown"
                print(f"{f['format_id']:<15} | {res:<10} | {f.get('format_note', '')}")

check_formats("https://www.tiktok.com/@sahalom_howladar/video/7562750709536410887?is_from_webapp=1&sender_device=pc")