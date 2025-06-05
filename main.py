import yt_dlp

def download_youtube_video(video_url, save_path="downloads"):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Download best video and audio and merge
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',  # Save file format
        'merge_output_format': 'mp4',  # Merge video and audio into MP4 format
        'noplaylist': True, # Only download the single video, not the whole playlist if it's part of one
    }
    try:
        print(f"Downloading: {video_url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Video downloaded successfully and saved in: {save_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_youtube_video(video_url)