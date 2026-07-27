import streamlit as st
import os
import time
import IPython as ip
import langchain
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from tavily import TavilyClient
import pytesseract as pyt
import numpy as np
from langchain.messages import SystemMessage, HumanMessage
from langchain.agents import create_agent

#===============front end======================
st.title("AI RESUME GENERATOR")

GOOGLE_API_KEY=st.sidebar.text_input("GOOGLE API KEY",type='password'
GROQ_API_KEY=st.sidebar.text_input("GROQ API KEY",type='password'
TAVILY_API_KEY=st.sidebar.text_input("TAVILY API KEY",type='password'

if not GOOGLE_API_KEY:
  st.warning("provide GOOGLE API KEY")

  def search_latest_news_jobs(query):
    """this function helps to get
  latest news or latest jobs
  related to user given query
  using tavily"""

  from tavily import TavilyClient
  client = TavilyClient(api_key=TAVILY_API_KEY)
  return client.search(query)

  model1 = ChatGoogleGenerativeAI(
   model = "gemini-3.5-flash-lite",
   google_api_key = GOOGLE_API_KEY
)
model2 = ChatGroq(
    model = "qwen/qwen3.6-27b",
    api_key = GROQ_API_KEY

    agent = create_agent(
    model = model1,
    tools = [search_latest_news_jobs]
)

def prompt generator():
  prompt = """You are a helpful Resume AI
  maler, i want you to use chain-of-thoughts
  and give detailed prompt for model
  where user want to generate resume
  for fresher or experienced one
  in html format, you have to give proper
  set of instructions, and make sure to keep
  design professional"""

  response = model1.invoke(prompt)
  prompt_ans = response.content[-1]['text']
  # print(prompt_ans)


  file_name = 'prompt.txt'
  with open(file_name, 'w') as f:
    f.write(prompt_ans)

prompt generator()

def prompt_reader():
  with open('prompt.txt','r') as f:
    prompt = f.read()
    return prompt

  prompt = """i want complete professional
  resume with dynamic design using advanced css and js
  and must show user input details
  system instructions: only give html code as output"""

  final_prompt = prompt + prompt_reader()
  profile_url = "https://s7d1.scene7.com/is/image/wbcollab/India_PM_Narendra_Modi-2?qlt=75&resMode=sharp2"
user_info = st.text_input("give user information:")
user_photo = st.sidebar.file_uploader("upload pic", type = 'image/jpeg')
  
user_query = f"""give resume for python developer
  user details : {user_info}
  use user profile image from given{user photo}"""
  
final_query = final_prompt + user_query

if st.button("generate resume"):
  with st.spinner("agent creating resume..."):
    resopnse = agent.invoke({'messages':[{'role':'user',"content":final_query}]})
    code = response['messages'][-1].content[-1]['text']
    st.html(code, width="stretch" , unsafe_allow_javascript=True)





