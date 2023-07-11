import streamlit as st

from langchain.chat_models import ChatAnthropic
from langchain.prompts.chat import *
from langchain.schema import *
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

import os

st.markdown("<h1 style='color: green;'>🍃 Meeting Summarizer</h1>", unsafe_allow_html=True)

st.markdown("""
<style>
.stTextInput input {
border-color: green !important;   
}
</style>
""", unsafe_allow_html=True)

password = st.text_input("Enter the password:", type="password")

if password == st.secrets["PASSWORD_KEY"]:

  api_key = st.secrets["ANTHROPIC_API_KEY"]
  os.environ["ANTHROPIC_API_KEY"] = api_key

  chat = ChatAnthropic(
    model="claude-2",
    max_tokens_to_sample=10000,
    streaming=True,  
    verbose=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
  )

  # Generate summary
  transcript = st.text_area("Please enter your transcript:")
  if transcript:
    nbm_template = """Summarize this call in  
    Current State:
    Future State: 
    Required Capabilities:
    Negative Consequences:
    Roles/Responsibilities:
    Format, make it detailed and business focused. Make sure you dont miss details mentioned in the call."""

    messages = [
      HumanMessage(content=f"""{nbm_template}, \\n\\n {transcript}""") 
    ]

    answer = chat(messages)
    summary = answer.content
    st.write(summary)

    # Chatbot for followup
    history = [summary] 
    while True:
      human_input = st.text_input("Ask a follow-up question:")
      if human_input:
        messages.append(HumanMessage(human_input))
        answer = chat(messages, history)
        bot_response = answer.content
        st.write(bot_response)
        history.append(human_input)
        history.append(bot_response)
      else:
        break

else:
  st.error("Incorrect password")
