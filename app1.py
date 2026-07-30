#====================load modules============================
import os
import time
import langchain
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from tavily import TavilyClient
import pytesseract as pyt
import numpy as np
import streamlit as st



#===========================API-KEYS=========================
GOOGLE_KEY = st.sidebar.text_input("Google-API",type = "password")
GROQ_KEY = st.sidebar.text_input("Groq-API",type = "password")
TAVILY_KEY = st.sidebar.text_input("Tavily-API",type = "password")

os.environ["GOOGLE_API_KEY"] = GOOGLE_KEY
os.environ["GROQ_API_KEY"] = GROQ_KEY
os.environ["TAVILY_API_KEY"] = TAVILY_KEY



ALL_API = [GOOGLE_KEY,   GROQ_KEY,  TAVILY_KEY]

if not all(ALL_API):
  st.sidebar.error("PASS API-KEYS")

elif any(ALL_API):
  st.sidebar.info("MUST PASS ALL KEYS")

else
st.sidebar.success("API KEYS LOADED SUCCESSFULLY")
# STEP1: MODEL CALL
model = ChatGoogleGenerativeAI(
  model = "gemini-3.5-flash lite",
  google_api_key = GOOGLE_API_KEY
)


#===========FRONTEND=========================
st.title("AI-Agent-Powered-ppt Generator")

user_query = st.text_area("write your ppt on prompt:")

#===============ASSESTS======================
# step2: tools creation
# tool_1

def search_latest_info(query):
  """this function search latest
  news or content from website
  using tavily, helpful to check
  trending content"""

  client = TavilyClient(api_key = TAVILY_API_KEY)
  response = client.search(query)
  return response


#Tool2
# tool 2:
def generate_image(img_prompt):
  """this function helps to generate image
  using free api, with given
  img_prompt using pollinations"""

  url = f"https://image.pollinations.ai/{img_prompt}"
  #file handling
  import requests as r
  content = r.get(url).content
  with open(f"Image.jpeg",'wb') as f:
    f.write(content)

  from PIL import Image
  return Image.open("Image.jpeg")

# with tabs
tab1, tab2, tab3 = st.tabs(["GENERATE IMAGE", 
                           "CHECK LATEST NEWS"
                           "GENERATE PPT"])

# detailed prompt generator
def prompt_generator(model,query):
  prompt = f"""your task is to give detailed prompt instructions
  for given

  prompt:
  you are a professional ppt generator, where
  user will give the query and based on that,
  you have to generate dynamic, html output based
  ppt with advanced css and dynamic ui and ux with
  ppt toggle button, based on query take image reference to generate
  and embed the same in ppt using
  Image ref: url = https://images.unsplash.com/photo, 
  or url = https://image.pollinations.ai/, 
  make sure img src must be valid, and image must be
  present inside html, Generate
  pollinations: url = https://image.pollinations.ai/img_prompt, generate
  with image caption, and no markdowns
  user query given below:{query}
  """

  response = model.invoke(prompt)
  final_prompt = response.content[-1]['text']

  with open("prompt.txt",'w') as f:
    f.write(final_prompt)
  return final_prompt

agent = create_agent(
model = model,
tools = [search_latest_info,
          generate image]
         )
# ==================display agent====================
st.sidebar.image(agent)

#==============with tabs======================
with tab1:
st.header("GENERATE IMAGE GIVE PROMPT")
if st.button("click to generate:")
with st.spinner("RUNNING AGENT):
  data = generate_image(user_query)
  st.image(data)
st.image("Image.Jpeg")

with tab2:
  st.header("CHECK LATEST NEWS")
  if st.button("FETCH NEWS"):
    with st.spinner("RUNNING AGENT.."):
      prompt = """give latest news india or world wide related
      to tech, buisness, jobs, or user requested output
      in proper html news templates """ +user_query
      response = agent.invoke({'messages':[{'role':"user",
                                      "content":prompt}]})

code = response['messages'][-1].content[-1]['text']

st.html(code, width = "stretch",
        unsafe_allow_javascript = True)

with tab3:
  st.header("GENERATE PPT")
  if st.button("CLICK TO GENERATE"):
    with st.spinner("RUNNING AGENT.."):
      final_prompt = prompt_generator(model, user_query)
      response = agent.invoke({'messages':[{'role':"user",
                                      "content":prompt}]})

code = response['messages'][-1].content[-1]['text']

st.html(code, width = "stretch",
        unsafe_allow_javascript = True)
st.download button(label = "DOWNLOAD PPT",
                   data = code,
                   file_name = ppt.html
                   mine = 'text/html')

                   st.success("PPT DOWNLOADED SUUCCESSFULLY")






  
        



                           

