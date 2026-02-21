import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
import uuid



if "threads" not in st.session_state:
    st.session_state.threads = {}   

if "current_thread" not in st.session_state:
    thread_id = str(uuid.uuid4())
    st.session_state.current_thread = thread_id
    st.session_state.threads[thread_id] = []



st.sidebar.title("💬 My Conversations")


if st.sidebar.button("Start New Chat"):
    new_thread_id = str(uuid.uuid4())
    st.session_state.current_thread = new_thread_id
    st.session_state.threads[new_thread_id] = []
    st.rerun()

st.sidebar.markdown("---")


for thread_id in st.session_state.threads.keys():
    if st.sidebar.button(f"Chat {thread_id[:8]}", key=thread_id):
        st.session_state.current_thread = thread_id
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("Current Thread:")
st.sidebar.code(st.session_state.current_thread)



message_history = st.session_state.threads[st.session_state.current_thread]


for message in message_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Type your message...")

if user_input:

   
    message_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    full_response = ""

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        for message_chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config={
                "configurable": {
                    "thread_id": st.session_state.current_thread
                }
            },
            stream_mode="messages"
        ):
            if message_chunk.content:
                full_response += message_chunk.content
                message_placeholder.markdown(full_response)

    message_history.append(
        {"role": "assistant", "content": full_response}
    )

  
    st.session_state.threads[st.session_state.current_thread] = message_history