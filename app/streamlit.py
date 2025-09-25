# Created by Devesh Singh (Demonforms)
import streamlit as st
from model import Model

@st.cache_resource
def load_model():
    """Loading the Chat Bot"""
    return Model()

model = load_model()

st.markdown("<h1 style='text-align: center; white-space: nowrap;'>Medical Chatbot</h1>",
            unsafe_allow_html=True)
st.markdown(
            f"<p style='text-align: center; font-size:14px; color:lightgray;'>"
            f"Project by <b>Devesh Singh</b>"
            f"</p>",
            unsafe_allow_html=True
        )

query = st.chat_input("Write your query")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if query:
    # Display the user's query in the chat message container
    with st.chat_message("user"):
        st.markdown(query)
    # Add the user's query to the session state
    st.session_state.messages.append({"role":"user", "content":query})

    response = model.ask(query, context = st.session_state.messages)

    # Display the response in the chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add the response to the session state
    st.session_state.messages.append({"role": "assistant", "content": response})


