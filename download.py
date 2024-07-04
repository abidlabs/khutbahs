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
        audio_stream = yt.streams.filter(only_audio=True).first()
        downloaded_file = audio_stream.download(AUDIO_DIR)
        base, _ = os.path.splitext(downloaded_file)
        mp3_file = Path(AUDIO_DIR) / (base + '.mp3')
        AudioSegment.from_file(downloaded_file).export(mp3_file, format='mp3')
        os.remove(downloaded_file)
        return mp3_file
    except Exception as e:
        warnings.warn(f"Cannot download {video_url}: {e}")

with open(URLS_FILE) as f:
    urls = f.readlines()
    for url in urls:
        print(f"Downloading: {url}")
        download_audio_from_youtube(url)
