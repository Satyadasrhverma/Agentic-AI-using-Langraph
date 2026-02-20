import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

import uuid

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input("Type your messages.....")

if user_input:
    
    st.session_state["message_history"].append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    
    full_response = ""

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        for message_chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config={"configurable": {"thread_id": st.session_state.thread_id}},
            stream_mode="messages"
        ):
            if message_chunk.content:
                full_response += message_chunk.content
                message_placeholder.markdown(full_response)

    
    st.session_state["message_history"].append(
        {"role": "assistant", "content": full_response}
    )