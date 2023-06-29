
import streamlit as st
from langchain.chat_models import ChatAnthropic
import os

# Use the secrets dict to access the secret value
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
chat = ChatAnthropic(model="claude-instant-1-100k", max_tokens_to_sample=10000)

# Use Streamlit to get the transcript from the user
transcript = st.text_input("Please enter your transcript: ")

# If the user has entered a transcript, process it
if transcript:
    nbm_template = "Summarize this call in current state, future state, required capabilities and negative consequences format, make it detailed and business focused. Highlight all details mentioned in the call."
    messages = [
        HumanMessage(content=f"""{nbm_template},  \n\n {transcript}""")
    ]
    answer = chat(messages)

    # Use Streamlit to display the summary
    st.write(answer.content)
