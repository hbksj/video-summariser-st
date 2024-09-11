from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder
from utils.prompts import CHATBOT_PROMPT
from utils.literals import LLAMA_70B,LLAMA_405B
import os
load_dotenv()

# initialize env variables
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")


## check if chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history=[]

## initialize output parser
output_parser=StrOutputParser()



## create prompt template
prompt= ChatPromptTemplate.from_messages([("system",CHATBOT_PROMPT),MessagesPlaceholder("chat_history"),("user","{input}")])



##Show Title
st.title("Chatbot")
with st.sidebar:
    selected_model=st.selectbox(options=[LLAMA_405B,LLAMA_70B],label="Choose Model")
    
## initialize LLM

if selected_model==LLAMA_70B:
    llm=ChatGroq(model='llama-3.1-70b-versatile')
elif selected_model==LLAMA_405B:
    llm = ChatNVIDIA(model='meta/llama-3.1-405b-instruct')
    
## initialize chain
conversation_chain= prompt | llm |output_parser

## Expaned for chat history
if st.session_state.chat_history:
    with st.expander("Chat History"):
        st.write(st.session_state.chat_history)
    

## run when user provide input to chat input field
if input:=st.chat_input(placeholder="Type something to chat"):
    chat_history=st.session_state.chat_history
    st.session_state.chat_history.extend([HumanMessage(input)])
    with st.spinner("..."):
        response=conversation_chain.invoke({"input":input,"chat_history":chat_history[-10:]})
        st.session_state.chat_history.extend([AIMessage(response)])
        st.success("Done")
        
        
## Display Chat History
if st.session_state.chat_history:
    for msgs in st.session_state.chat_history:
        role = "user" if type(msgs) is HumanMessage else "ai"
        st.chat_message(role).write(msgs.content)
    