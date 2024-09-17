from deepgram import DeepgramClient, SpeakOptions
from dotenv import load_dotenv
import streamlit as st
import io
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

SYSTEM_TEMPLATE = """
Rewrite the provided input text to sound like a casual, conversational tone, as if speaking directly to Instagram followers. 
Introduce natural-sounding pauses, filler words (e.g., 'uh', 'um'), and emotional expressions to enhance the tone, without altering the original meaning, grammar, syntax, or word choice.

Requirements:

Leave the original text completely unchanged, including all words, phrases, grammar, syntax, and word choice
Add commas to indicate natural breaks in speech, as needed
Use ellipses (...) to indicate longer breaks in speech, only when necessary
Incorporate filler words like 'Uh' and 'um' to indicate hesitation or pause and emotional expressions to create a conversational tone, while preserving the original text's integrity
Change the below texts into their actual pronounciation - 
    Nueravi -> Newravi

Remember not to change the original text at all. And dont include any messages or notes or anything else that indicates it is rewritten text.
"""
USER_TEMPLATE = """
Input : {input}
"""

llm = ChatGroq(model="llama-3.1-70b-versatile")

output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages([("system",SYSTEM_TEMPLATE),("user",USER_TEMPLATE)])

chain = prompt | llm | output_parser
with st.sidebar:
    model_value = st.selectbox(
        "Choose Voice",
        options=[
            "aura-asteria-en",
            "aura-orpheus-en",
            "aura-athena-en",
            "aura-helios-en",
            "aura-hera-en",
            "aura-stella-en",
            "aura-luna-en",
            "aura-orion-en",
            "aura-perseus-en",
            "aura-zeus-en",
            "aura-angus-en",
        ],
    )
    speech_flow=st.radio(label="Speech Flow",options={"ORIGINAL","NATURAL"})
    
if input := st.chat_input("Enter text"):

    filename = "output.wav"
    try:
        if speech_flow=="NATURAL":
            response_text = chain.invoke({"input": input})
            with st.expander("Text"):
                st.write(f"Original : {input}")
                st.write(f"Modified : {response_text}")
        else:
            response_text=input

        SPEAK_OPTIONS = {"text": response_text}
        deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(model=model_value)

        # STEP 3: Call the save method on the speak property
        with st.spinner():
            response: DeepgramClient = deepgram.speak.rest.v("1").save(
                filename, SPEAK_OPTIONS, options
            )
            audio = open(filename, "rb").read()
            if audio:
                st.audio(data=io.BytesIO(audio),autoplay=True)
                st.download_button(
                    "Download", data=io.BytesIO(audio), file_name=filename
                )
            st.success("Done")

    except Exception as e:
        print(f"Exception: {e}")

    except Exception as e:
        print(f"Exception: {e}")
