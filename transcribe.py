import whisper
import os
from pathlib import Path

AUDIO_DIR = "audios"
RAW_TRANSCRIPTS_DIR = "raw_transcripts"

model = whisper.load_model("large-v3")

for audio_file in os.listdir(AUDIO_DIR):
    if audio_file.endswith(".mp3"):
        print("Transcribing: ", audio_file)
        raw_transcript_file = Path(RAW_TRANSCRIPTS_DIR) / (Path(audio_file).with_suffix('').name + ".txt")
        if not Path(raw_transcript_file).exists():
            result = model.transcribe(AUDIO_DIR + "/" + audio_file, verbose=False, language="en")
            with open(raw_transcript_file, "w") as f:
                f.write(result["text"])
