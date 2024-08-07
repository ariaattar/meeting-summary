import streamlit as st
import anthropic
import os

st.markdown("<h1 style='color: green;'>🍃 Meeting Summarizer</h1>", unsafe_allow_html=True)

st.markdown("""
<style>
.stTextInput input {
    border-color: green !important;
}
</style>
""", unsafe_allow_html=True)

api_key = os.environ.get("ANTHROPIC_API_KEY")
password_key = os.environ.get("PASSWORD_KEY", "nbm")  

password = st.text_input("Enter the password:", type="password")

if password == password_key:
    if not api_key:
        st.error("ANTHROPIC_API_KEY is not set in the environment variables.")
    else:
        client = anthropic.Anthropic(api_key=api_key)

        transcript = st.text_input("Please enter your transcript: ")
        question = st.text_area("Please enter your question: ")
        if st.button("Summarize in MongoDB Format"):
            question = """Summarize this call in a way that collects all of this info:

            Current state, future state, required capabilities, timeline/deadline, pain/goal/need? 

            """
        if transcript and question:
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=4000,
                temperature=0.2,
                system="Based on this sales call, help answer the user's question.",
                messages=[
                    {
                        "role": "user",
                        "content": f"Transcript: {transcript}\n\nQuestion: {question}"
                    }
                ]
            )

            # Parse and display the response
            if isinstance(message.content, list):
                for item in message.content:
                    if hasattr(item, 'text'):
                        st.write(item.text)
                    elif isinstance(item, dict) and 'text' in item:
                        st.write(item['text'])
                    else:
                        st.write(str(item))
            else:
                st.write(message.content)
else:
    st.error("The password you entered is incorrect. Please try again.")
