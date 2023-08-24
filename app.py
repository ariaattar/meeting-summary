import streamlit as st
from langchain.chat_models import ChatAnthropic
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

    from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        AIMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )
    from langchain.schema import (
        AIMessage,
        HumanMessage,
        SystemMessage
    )
    chat = ChatAnthropic(
        model="claude-instant-1.2", 
        max_tokens_to_sample=10000,
        streaming=True,
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    transcript = st.text_input("Please enter your transcript: ")
    question = st.text_area("Please enter your question: ")

    
    if transcript and question:
        nbm_template = """
        
        Based on this sales call help answer the users question
        
        ."""
        messages = [
            HumanMessage(content=f"""{nbm_template},  \n\n {transcript}, \n\n {question}""")
        ]
        answer = chat(messages)

        st.write(answer.content)
else:
    st.error("The password you entered is incorrect. Please try again.")
