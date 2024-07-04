import os
from huggingface_hub import InferenceClient
from pathlib import Path
import tqdm
import difflib
import string

RAW_TRANSCRIPTS_DIR = "raw_transcripts"
CLEAN_TRANSCRIPTS_DIR = "clean_transcripts"
MODEL_NAME = "meta-llama/Meta-Llama-3-70b-Instruct"
PROMPT = """
The following is a raw transcript from an automatic transcription system. Break
it into paragraphs based on logical structure. Don't change or add any words.
"""
PREFIX_LENGTH = 50

def split_text_into_chunks(text: str, chunk_size=1000):
    words = text.split(' ')
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def remove_prefix(generated_text, original_text):
    no_whitespace_original_text = "".join(char for char in original_text if char not in string.whitespace)
    matching_counter = 0
    start_counter = 0
    match = False
    for i in range(len(generated_text)):
        if matching_counter == len(no_whitespace_original_text):
            break
        if generated_text[i] in string.whitespace:
            continue
        if generated_text[i] != no_whitespace_original_text[matching_counter]:
            matching_counter = 0
            start_counter = i + 1
            match = False
        else:
            match = True
            matching_counter += 1
    if match:
        return generated_text[start_counter:]
    else:
        return generated_text

def clean_transcript(file_name):
    text = f"# {Path(file_name).with_suffix('').name}\n\n"
    transcript = open(file_name, "r").read()
    chunks = split_text_into_chunks(transcript)
    for chunk in tqdm.tqdm(chunks):
        messages = [
            {"role": "user", "content": PROMPT + "\n" + chunk}
        ]
        client = InferenceClient(model=MODEL_NAME)
        c = client.chat_completion(messages, max_tokens=4000)
        token = c.choices[0].message.content
        token = remove_prefix(token, chunk[:PREFIX_LENGTH])
        text += token + " "
    return text    

for transcript_file in os.listdir(RAW_TRANSCRIPTS_DIR):
    if transcript_file.endswith(".txt"):
        print("Cleaning: ", transcript_file)
        clean_transcript_file = Path(CLEAN_TRANSCRIPTS_DIR) / (Path(transcript_file).with_suffix('').name + ".md")
        if not Path(clean_transcript_file).exists():
            clean = clean_transcript(RAW_TRANSCRIPTS_DIR + "/" + transcript_file)
            with open(clean_transcript_file, "w") as f:
                f.write(clean)
