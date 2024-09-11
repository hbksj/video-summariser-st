import os
from groq import Groq
from langchain_groq import ChatGroq
from langchain_nvidia_ai_endpoints import ChatNVIDIA
import pdfplumber
from langchain.document_loaders import YoutubeLoader

from utils.literals import LLAMA_405B, LLAMA_70B
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

def get_transcript(input_url:str,url_content):
    if not url_content:
        return YoutubeLoader.from_youtube_url(input_url,language=["en", "hi","es",],).load()
    else:
        return url_content
    
    
def get_seletec_llm(model:str):
    ## initialize LLM
    if model==LLAMA_70B:
        llm=ChatGroq(model='llama-3.1-70b-versatile')
    elif model==LLAMA_405B:
        llm = ChatNVIDIA(model='meta/llama-3.1-405b-instruct')
    return llm