import os
from groq import Groq
import pdfplumber
client = Groq()

## function to get audio transcript
def get_audio_transcript(file_name:str,file)->str:
    file_path=os.path.splitext(file_name)[1]
    transcription = client.audio.transcriptions.create(
    file=(file_path,file.read()),
    model="distil-whisper-large-v3-en",
    prompt="Transcript",
    response_format="verbose_json",
    )
    return transcription.text

## Function to read pdf
def read_pdf(file)->str:
    with pdfplumber.open(file) as pdf:
            text=""
            for page in pdf.pages:
                text+=page.extract_text()
    return text