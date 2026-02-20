from langgraph.graph import StateGraph, START,END
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
) 

model = ChatHuggingFace(llm = llm)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat(state:ChatState):
    messages = state['messages']
    result = model.invoke(messages)

    return {'messages' : [result]}

pointer = InMemorySaver()

graph = StateGraph(ChatState)

graph.add_node("chat_node" , chat)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=pointer)