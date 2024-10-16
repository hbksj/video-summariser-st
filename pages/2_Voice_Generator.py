from deepgram import DeepgramClient, SpeakOptions
from dotenv import load_dotenv
import streamlit as st
import io
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from utils.literals import LLAMA_70B
from utils.utils import get_seletec_llm
import boto3
from pages.utils.voice_list import VoiceList
from pages.utils.voice_prompts import SYSTEM_TEMPLATE
import os

load_dotenv()

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

llm = get_seletec_llm(LLAMA_70B)

output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_TEMPLATE), ("user", "Input : {input}")]
)
chain = prompt | llm | output_parser
with st.sidebar:
    st.session_state.voice_engine = st.selectbox(
        label="Voice Engine", options=["generative", "long-form", "neural","standard"]
    )
    speech_flow = st.selectbox(
        label="Speech Flow", options=["Normal", "Natural"]
    ) if st.session_state.voice_engine =="standard" else st.empty()
    st.session_state.voice_id = st.selectbox(
        "Choose Voice",
        options={
            "generative": sorted(VoiceList.voices_generative),
            "long-form": sorted(VoiceList.voices_longform),
            "standard": sorted(VoiceList.voices_standard)
            
        }.get(st.session_state.voice_engine, []),
    )


if input := st.chat_input("Enter text"):

    filename = "output.mp3"
    try:
        if speech_flow=="Natural":
            response_text = chain.invoke({"input": input})
        else:   
            response_text = input
        with st.expander("Text"):
            st.write(response_text)
        with st.spinner():
            try:
                response = client.synthesize_speech(
                    Engine=st.session_state.voice_engine,
                    LanguageCode="en-IN",
                    OutputFormat="mp3",
                    Text=response_text,
                    TextType="ssml" if (st.session_state.voice_engine=="standard" and speech_flow=="Natural") else "text",
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
