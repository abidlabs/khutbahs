from pytube import YouTube
import os
from pydub import AudioSegment
import warnings
from pathlib import Path

URLS_FILE = "urls.txt"
AUDIO_DIR = "audios"

def download_audio_from_youtube(video_url):
    try:
        yt = YouTube(video_url)
        title = yt.title
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        mp3_file = Path(AUDIO_DIR) / f"{safe_title}.mp3"
        if mp3_file.exists():
            return mp3_file
        audio_stream = yt.streams.filter(only_audio=True).first()
        downloaded_file = audio_stream.download(AUDIO_DIR)
        AudioSegment.from_file(downloaded_file).export(mp3_file, format='mp3')
        os.remove(downloaded_file)
        return mp3_file
    except Exception as e:
        warnings.warn(f"Cannot download {video_url}: {e}")

Path(AUDIO_DIR).mkdir(parents=True, exist_ok=True)

with open(URLS_FILE) as f:
    urls = f.readlines()
    for url in urls:
        print(f"Downloading: {url.strip()}")
        download_audio_from_youtube(url)
