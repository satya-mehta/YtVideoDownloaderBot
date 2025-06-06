import yt_dlp
import time
import os
import shutil

def get_writable_cookie_file():
    source_path = '/etc/secrets/cookies.txt'
    temp_path = '/tmp/cookies.txt'
    
    # Copy the file from the secure (read-only) location to /tmp
    shutil.copyfile(source_path, temp_path)
    return temp_path

def download_youtube_video(video_url, save_path="downloads", audvid=True):
    cookie_file = get_writable_cookie_file()
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best' if audvid else 'bestaudio/best',  # Download best video and audio and merge
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',  # Save file format
        #'merge_output_format': 'mp4' if audvid else 'mp3',  # Merge video and audio into MP4 format
        'noplaylist': True, # Only download the single video, not the whole playlist if it's part of one
        'cookiefile': cookie_file,  # Use the secure file path
        'http_headers': {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/96.0.4664.55 Safari/537.36'
            )
        },
    }
    if audvid:
        ydl_opts['merge_output_format'] = 'mp4'  # Ensure video + audio is merged into MP4
    else:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Convert to MP3
            'preferredquality': '320',  # Set bitrate quality
        }]

    try:
        time.sleep(2)
        print(f"Downloading: {video_url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)

            final_path = ydl.prepare_filename(info_dict)
            
            if not audvid:
                final_path = os.path.splitext(final_path)[0] + '.mp3'
        print(f"Video downloaded successfully and saved in: {final_path}")
        return final_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# if __name__ == "__main__":
#     video_url = input("Enter the YouTube video URL: ")

#     download_youtube_video(video_url, audvid=False)