from deepgram import DeepgramClient, SpeakOptions
from dotenv import load_dotenv
import streamlit as st
import io
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from utils.literals import LLAMA_405B
from utils.utils import get_seletec_llm
import boto3
from pages.utils.voice_list import VoiceList
import os

load_dotenv()


st.write(f"{os.getenv("AWS_ACCESS_KEY_ID")} {os.getenv("AWS_SECRET_ACCESS_KEY")}")
session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION"),
)

client = session.client("polly")

if "voice_engine" not in st.session_state:
    st.session_state.voice_engine = "generative"
if "voice_id" not in st.session_state:
    st.session_state.voice_id = ""
# SYSTEM_TEMPLATE = """
# Rewrite the provided input text to sound like a casual, conversational tone, as if speaking directly to Instagram followers.
# Introduce natural-sounding pauses, filler words (e.g., 'uh', 'um'), and emotional expressions to enhance the tone, without altering the original meaning, grammar, syntax, or word choice.

# Requirements:

# Leave the original text completely unchanged, including all words, phrases, grammar, syntax, and word choice
# Add commas to indicate natural breaks in speech, as needed
# Use ellipses (...) to indicate longer breaks in speech, only when necessary
# Incorporate filler words like 'Uh' and 'um' to indicate hesitation or pause and emotional expressions to create a conversational tone, while preserving the original text's integrity
# Change the below texts into their actual pronounciation -
#     Nueravi -> Newravi

# Remember :
# To not change the original text at all. And dont include any messages or notes or anything else that indicates it is rewritten text.
# To not change meaning of the input at all in any way.
# To not add in brackets pauses or anything other indicating the action done ; example - (pauses)

# """
# USER_TEMPLATE = """
# Input : {input}
# """

llm = get_seletec_llm(LLAMA_405B)

output_parser = StrOutputParser()
# prompt = ChatPromptTemplate.from_messages(
#     [("system", SYSTEM_TEMPLATE), ("user", USER_TEMPLATE)]
# )
# chain = prompt | llm | output_parser
with st.sidebar:
    st.session_state.voice_engine = st.selectbox(
        label="Voice Engine", options=["generative", "long-form", "neural"]
    )
    st.session_state.voice_id = st.selectbox(
        "Choose Voice",
        options={
            "generative": sorted(VoiceList.voices_generative),
            "long-form": sorted(VoiceList.voices_longform),
        }.get(st.session_state.voice_engine, []),
    )


if input := st.chat_input("Enter text"):

    filename = "output.mp3"
    try:
        response_text = input

        # SPEAK_OPTIONS = {"text": response_text}
        # deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        # options = SpeakOptions(model=voice_id)

        # STEP 3: Call the save method on the speak property
        with st.spinner():
            try:
                response = client.synthesize_speech(
                    Engine=st.session_state.voice_engine,
                    LanguageCode="en-IN",
                    OutputFormat="mp3",
                    Text=response_text,
                    TextType="text",
                    VoiceId=st.session_state.voice_id,
                )
                with open(filename, "wb") as audio_file:
                    audio_file.write(response["AudioStream"].read())
                audio = open(filename, "rb").read()
                if audio:
                    st.audio(data=io.BytesIO(audio), autoplay=True)
                    st.download_button(
                        "Download", data=io.BytesIO(audio), file_name=filename
                    )
                st.success("Done")
            except Exception as e:
                st.error(e)

    except Exception as e:
        print(f"Exception: {e}")

    except Exception as e:
        print(f"Exception: {e}")
