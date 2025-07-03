import streamlit as st
from PyPDF2 import PdfReader
# from langchain.chains import ConversationChain
# from langchain.memory import ConversationBufferMemory
# from langchain_community.llms import Ollama
import os

os.environ["OLLAMA_HOME"] = "/app/.ollama"


st.set_page_config(page_title="Career Mentor AI", layout="centered")  # getting web page ready for the chat front end interface
st.title("AI Mentor Career ChatBot")

# llm = Ollama(model="llama3")
# conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory())  #stores the llm models and its memory

if "resume_text" not in st.session_state:    # gives the session storage in resume text or chat history
    st.session_state.resume_text = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

resume_file = st.file_uploader("Upload your resume (PDF) — optional", type=["pdf"])   # gives the option to upload resumes to extract data gives solution as per users input
if resume_file is not None:
    reader = PdfReader(resume_file)
    st.session_state.resume_text = ""
    for page in reader.pages:
        st.session_state.resume_text += page.extract_text()

st.subheader("Enter Your Queries based on your career program")

with st.form("career_form", clear_on_submit=True):
    user_query = st.text_input("Type your question (e.g., 'How do I move from sales to data analytics?')", key="input_query")
    submitted = st.form_submit_button("Get Advice")  

import requests

API_KEY = "AIzaSyA6JWnxYTlLJVkZxBrxklLXrzNlsP_abIE" 

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}




if submitted and user_query:
    context = ""
    if st.session_state.resume_text:
        context += f"Resume:\n{st.session_state.resume_text.strip()}\n"
    context += f"Question: {user_query.strip()}"

    with st.spinner("Thinking..."):
        # response = conversation.run(context)
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": context
                        }
                    ]
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        data = response.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"]

        # st.session_state.chat_history.append((user_query, response))
        st.session_state.chat_history.append((user_query, text))

        st.success("✅ Here's your personalized career advice:")
        st.markdown(f"**User:** {user_query}")
        # st.markdown(f"**AI Mentor:** {response}")
        st.markdown(f"**AI Mentor:** {text}")
        st.markdown("---")

if st.session_state.chat_history:
    st.subheader("Conversation History")
    for q, a in st.session_state.chat_history[:-1]:  # this saves and update the history of most recent ones 
        st.markdown(f"**User:** {q}")
        st.markdown(f"**AI Mentor:** {a}")
        st.markdown("---")# trigger rebuild
