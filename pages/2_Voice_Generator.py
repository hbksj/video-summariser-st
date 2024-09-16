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
Take the input and totally make it sound like, you know, I'm talking to you right now. Use ... to add in some pauses, filler words like 'um' and 'uh', and emotional expressions, without changing the original words or meaning. 
Leave the original text intact, including grammar, syntax, and word choice... but, like, add in some subtle breaks and hesitations to create a more spontaneous and human-like tone. 
You can use commas to indicate natural breaks... and, you know, dots to indicate longer breaks in speech... only where necessary, though. Also, throw in some filler words to simulate a natural flow. 
Don't alter the original text in any way... just, like, add to it to create a more natural-sounding script. 
Stick to the original text input, no matter what... 
I want it to sound like I'm speaking directly to my followers on Instagram
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
if input := st.chat_input("Enter text"):

    filename = "output.wav"
    try:
        response_text = chain.invoke({"input": input})
        with st.expander("Text"):
            st.write(f"Original : {input}")
            st.write(f"Modified : {response_text}")

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
