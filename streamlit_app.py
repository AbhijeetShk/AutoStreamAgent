import streamlit as st
from graph import build_graph

st.set_page_config(page_title="AutoStream Assistant", page_icon="☕️")
st.title("AutoStream Assistant")
st.caption("AI-powered lead generation demo")

if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

if "state" not in st.session_state:
    st.session_state.state = {"messages": []}

if "chat" not in st.session_state:
    st.session_state.chat = []

with st.sidebar:
    st.header("Controls")
    if st.button("Reset Chat"):
        st.session_state.state = {"messages": []}
        st.session_state.chat = []
        st.rerun()

for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.write(msg)

prompt = st.chat_input("Ask about pricing, features, or get started...")

if prompt:
    st.session_state.chat.append(("user", prompt))
    with st.chat_message("user"):
        st.write(prompt)

    result = st.session_state.graph.invoke({
        **st.session_state.state,
        "user_input": prompt
    })

    st.session_state.state = result
    reply = result["reply"]

    st.session_state.chat.append(("assistant", reply))
    with st.chat_message("assistant"):
        st.write(reply)