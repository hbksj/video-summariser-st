from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.document_loaders import UnstructuredURLLoader
from langchain_community.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
import streamlit as st
import validators
from utils.utils import get_audio_transcript,read_pdf,get_transcript
from utils.prompts import SUMMARIZER_PROMPT
from utils.literals import AUDIO_SUMMARIZER,YOUTUBE_SUMMARIZER,URL_SUMMARIZER,WIKIPEDIA,PDF_SUMMARIZER,TEXT_SUMMARIZER
from dotenv import load_dotenv
import os
load_dotenv()
# initialize env variables
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

wikipedia=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1))

llm = ChatGroq(model='llama-3.1-70b-versatile')

output_parser=StrOutputParser()

prompt_template=ChatPromptTemplate.from_template(SUMMARIZER_PROMPT)

chain = prompt_template | llm | output_parser


file=None
                
st.title("Summarizer")
with st.sidebar:
    drop_down=st.selectbox("Choose a source",options=(YOUTUBE_SUMMARIZER,URL_SUMMARIZER,WIKIPEDIA,PDF_SUMMARIZER,AUDIO_SUMMARIZER,TEXT_SUMMARIZER))
    drop_down_language=st.selectbox("Summary Language",options=("English","Hindi","French","Spanish","Bengali","Mathili"))
    min_word_length=st.slider("Min Word Length",min_value=100,max_value=2000,step=100)
    max_word_length=st.slider("Max Word Length",min_value=100,max_value=2000,step=100,value=min_word_length)
 
        
 
   
if drop_down in [AUDIO_SUMMARIZER, PDF_SUMMARIZER]:
    file = st.file_uploader("Upload Files", type=["mp3,m4a","ogg","mpeg","audio/mpeg","audio/mpg",] if drop_down == AUDIO_SUMMARIZER else "pdf")
    input_url = ""
elif drop_down in [WIKIPEDIA,TEXT_SUMMARIZER]:
    input_url = st.text_area("Summarizer Text")
else:
    input_url = st.text_input("Enter URL")
    

if submit:=st.button("Submit"):
    if (input_url is not None and len(input_url)>0) or drop_down==PDF_SUMMARIZER  or drop_down ==AUDIO_SUMMARIZER:
        try: 
            if drop_down not in [WIKIPEDIA ,PDF_SUMMARIZER ,AUDIO_SUMMARIZER,TEXT_SUMMARIZER] and not validators.url(input_url):
                st.error("Not a valid url")
            else:
                with st.spinner(text="Loading...."):
                    ## if selected drop down is YOUTUBE_SUMMARIZER for the source
                    
                    if drop_down==YOUTUBE_SUMMARIZER:
                        url_content=""
                        url_content=get_transcript(input_url=input_url,url_content=url_content)
                        
                    ## if selected drop down is URL_SUMMARIZER for the source
                    elif drop_down==URL_SUMMARIZER:
                        url_content=UnstructuredURLLoader(urls=[input_url]).load()
                        
                    ## if selected drop down is wikipedia for the source
                    elif drop_down==WIKIPEDIA:
                        url_content=wikipedia.run(input_url)
                        
                    ## if selected drop down is Text Summarizer for the source
                    elif drop_down==TEXT_SUMMARIZER:
                        url_content=input_url
                    
                     ## if selected drop down is PDF_SUMMARIZER for the source
                    elif drop_down==PDF_SUMMARIZER:
                        url_content=read_pdf(file)
                    
                    ## if selected drop down is Audio summarizer for the source
                    elif drop_down==AUDIO_SUMMARIZER:
                        url_content=get_audio_transcript(file_name=file.name,file=file)
                    
                    ## Expandable content with title URL Content
                    with st.expander("URL Content"):
                        st.write(url_content)
                    
                    ## Stream the input from chain
                    st.write_stream(chain.stream({"input":url_content,"language":drop_down_language,"min_word_length":min_word_length,"max_word_length":max_word_length}))
                    
                    ## Show success message
                    st.success("Done")
                

        except Exception as e:
            st.error(e)
    else:
        st.error("URL cannot be empty")

