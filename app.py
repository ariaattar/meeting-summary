import streamlit as st
from langchain.chat_models import ChatAnthropic
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
    chat = ChatAnthropic(model="claude-1.3-100k", max_tokens_to_sample=10000)

    transcript = st.text_input("Please enter your transcript: ")

    if transcript:
        nbm_template = "Summarize this call in current state, future state, required capabilities and negative consequences format, make it detailed and business focused. Highlight all details mentioned in the call."
        messages = [
            HumanMessage(content=f"""{nbm_template},  \n\n {transcript}""")
        ]
        answer = chat(messages)

        st.write(answer.content)
else:
    st.error("The password you entered is incorrect. Please try again.")
