from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.document_loaders import YoutubeLoader,UnstructuredURLLoader,PyMuPDFLoader
from langchain_community.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
import pdfplumber
import streamlit as st
import validators

wikipedia=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1))

llm = ChatGroq(model='llama-3.1-70b-versatile')


prompt="""
Summarize the below content input on the below guidelines:
- The minimum length of the summary should strictly be {min_word_length}. 
- The maximum length of the summary should strictly be {max_word_length}. 

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
with st.sidebar:
    drop_down=st.selectbox("Choose a source",options=(YOUTUBE_SUMMARIZER,URL_SUMMARIZER,WIKIPEDIA,PDF_SUMMARIZER))
    drop_down_language=st.selectbox("Summary Language",options=("English","Hindi","French","Spanish","Bengali","Mathili"))
    min_word_length=st.slider("Min Word Length",min_value=100,max_value=2000,step=100)
    max_word_length=st.slider("Max Word Length",min_value=100,max_value=2000,step=100,value=min_word_length)
    
file=None
if drop_down==PDF_SUMMARIZER:
    file=st.file_uploader("Upload Files",type="pdf")
    input_url=""
elif drop_down==WIKIPEDIA:
    input_url=st.text_area("Search to summarize")
else:
    input_url=st.text_input("Enter URL")


if file is not None:
    pdf_text=read_pdf(file)
    

submit=st.button("Submit")

if submit:
    if (input_url is not None and len(input_url)>0) or drop_down==PDF_SUMMARIZER :
        try: 
            if not validators.url(input_url) and drop_down != WIKIPEDIA and drop_down!=PDF_SUMMARIZER:
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
                        url_content=pdf_text
                    
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

