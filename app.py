import streamlit as st
from langchain.chat_models import ChatAnthropic
from langchain.prompts.chat import * 
from langchain.schema import *
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os

st.set_page_config(page_title="Meeting Summarizer", page_icon="📝") 
st.title("Meeting Summarizer 📝")


password = st.text_input("Enter password:", type="password")
if password != st.secrets["password"]:
  st.error("Incorrect password")
  st.stop()


api_key = st.secrets["ANTHROPIC_API_KEY"]
os.environ["ANTHROPIC_API_KEY"] = api_key

chat = ChatAnthropic(
  model="claude-2",
  max_tokens_to_sample=1000,
  verbose=True,
  callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

transcript = st.text_area("Enter transcript:")
if transcript:

  summary = generate_summary(transcript, chat)
  st.write(summary)


history = [summary]
while True:
  question = st.text_input("Ask a follow-up question:")
  if question:
    history.append(str(question)) 
    response = chat.ask(question, history)
    st.write(response)
    history.append(str(response))
  else:
    break
