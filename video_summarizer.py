from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.document_loaders import YoutubeLoader,UnstructuredURLLoader,PyMuPDFLoader
from langchain_community.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
import pdfplumber
import streamlit as st
import validators
from dotenv import load_dotenv

load_dotenv()

wikipedia=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1))

llm = ChatGroq(model='llama-3.1-70b-versatile')


import os
from groq import Groq

client = Groq()

def get_audio_transcript(file_name:str,file)->str:
    file_path=os.path.splitext(file_name)[1]
    transcription = client.audio.transcriptions.create(
    file=(file_path,file.read()),
    model="distil-whisper-large-v3-en",
    prompt="Transcript",
    response_format="verbose_json",
    )
    return transcription.text
    

prompt="""
Summarize the below content input on the below guidelines:
- The minimum word count of the summary should strictly be {min_word_length} words. 
- The maximum word count of the summary should strictly be {max_word_length} words.
- Show the number of words at the end of summary.

Input :  {input}

Also detect the language of the transcript and let the user know the language.

Also provide summary in below language if language is not empty else provide in english.

Language : {language}

Note: 
- Dont let the user know what input content you are using.
- Only the summary part should be in the selected language , the other information should remain in english.
"""

output_parser=StrOutputParser()

prompt_template=ChatPromptTemplate.from_template(prompt)

chain = prompt_template | llm | output_parser


def read_pdf(file)->str:
    with pdfplumber.open(file) as pdf:
            text=""
            for page in pdf.pages:
                text+=page.extract_text()
    return text
                
st.title("Summarizer")



YOUTUBE_SUMMARIZER="Youtube summarizer"
URL_SUMMARIZER="URL Summarizer"
WIKIPEDIA = "Wikipedia"
PDF_SUMMARIZER="PDF SUMMARIZER"
AUDIO_SUMMARIZER="Audio Summarizer"
with st.sidebar:
    drop_down=st.selectbox("Choose a source",options=(YOUTUBE_SUMMARIZER,URL_SUMMARIZER,WIKIPEDIA,PDF_SUMMARIZER,AUDIO_SUMMARIZER))
    drop_down_language=st.selectbox("Summary Language",options=("English","Hindi","French","Spanish","Bengali","Mathili"))
    min_word_length=st.slider("Min Word Length",min_value=100,max_value=2000,step=100)
    max_word_length=st.slider("Max Word Length",min_value=100,max_value=2000,step=100,value=min_word_length)
    
file=None
if drop_down in [AUDIO_SUMMARIZER, PDF_SUMMARIZER]:
    file = st.file_uploader("Upload Files", type=["mp3,m4a","ogg"] if drop_down == AUDIO_SUMMARIZER else "pdf")
    input_url = ""
elif drop_down == WIKIPEDIA:
    input_url = st.text_area("Search to summarize")
else:
    input_url = st.text_input("Enter URL")
    

submit=st.button("Submit")

if submit:
    if (input_url is not None and len(input_url)>0) or drop_down==PDF_SUMMARIZER  or drop_down ==AUDIO_SUMMARIZER:
        try: 
            if not validators.url(input_url) and drop_down != WIKIPEDIA and drop_down!=PDF_SUMMARIZER and drop_down !=AUDIO_SUMMARIZER:
                st.error("Not a valid url")
            else:
                with st.spinner(text="Loading...."):
                    ## if selected drop down is YOUTUBE_SUMMARIZER for the source
                    if drop_down==YOUTUBE_SUMMARIZER:
                        url_content=YoutubeLoader.from_youtube_url(input_url,language=["en", "hi"],).load()
                        
                    ## if selected drop down is URL_SUMMARIZER for the source
                    elif drop_down==URL_SUMMARIZER:
                        url_content=UnstructuredURLLoader(urls=[input_url]).load()
                        
                    ## if selected drop down is wikipedia for the source
                    elif drop_down==WIKIPEDIA:
                        url_content=wikipedia.run(input_url)
                    
                     ## if selected drop down is PDF_SUMMARIZER for the source
                    elif drop_down==PDF_SUMMARIZER:
                        url_content=read_pdf(file)
                    elif drop_down==AUDIO_SUMMARIZER:
                        url_content=get_audio_transcript(file_name=file.name,file=file)
                    
                    ## Expandable content with title URL Content
                    with st.expander("URL Content"):
                        st.write(url_content)
                    
                    ## Stream the input from chain
                    st.write_stream(chain.stream({"input":url_content,"language":drop_down_language,"min_word_length":min_word_length,"max_word_length":max_word_length}))
                    
                    ## Show success message
                    st.success("Hooray!!!")
                

        except Exception as e:
            st.error(e)
    else:
        st.error("URL cannot be empty")

