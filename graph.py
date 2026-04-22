from langgraph.graph import StateGraph, END
from state import AgentState
from llm import llm
from rag import search_docs
from tools import mock_lead_capture

INVALID_NAME_WORDS = {
    "pricing",
    "plans",
    "get started",
    "autostream",
    "pro",
    "basic",
    "youtube",
    "instagram"
}

def classify(state: AgentState):
    prompt = f"""
Classify message into one label only:

greeting
pricing
lead
general

pricing includes:
- asking plans
- asking features
- asking recommendation between plans
- asking which plan suits them
- asking based on usage volume

lead means clear intent to buy/start/signup.

Message: {state['user_input']}

Return only label.
"""
    label = llm.invoke(prompt).content.strip().lower()
    state["intent"] = label
    return state


def router(state: AgentState):
    if state.get("mode") == "collecting":
        return "collect"

    state = classify(state)
    label = state["intent"]

    if "greeting" in label:
        return "greet"

    if "pricing" in label:
        return "rag"

    if "lead" in label:
        return "lead"

    return "general"


def greet_node(state: AgentState):
    state["reply"] = "Hey! I can help with pricing, plans or getting started with AutoStream."
    return state


def rag_node(state: AgentState):
    context = search_docs(state["user_input"])

    prompt = f"""
Use only this context to answer:

{context}

Question: {state['user_input']}

Keep answer concise and natural.
"""

    state["reply"] = llm.invoke(prompt).content
    return state


def lead_node(state: AgentState):
    state["mode"] = "collecting"
    state["reply"] = "Sounds good. What should I call you?"
    return state


def collect_node(state: AgentState):
    msg = state["user_input"].strip()
    lower_msg = msg.lower()

    if not state.get("name"):
        if lower_msg in INVALID_NAME_WORDS or len(msg) < 2:
            state["reply"] = "I meant your name so I can register you properly."
            return state

        state["name"] = msg
        state["reply"] = "Thanks. What's your email?"
        return state

    if not state.get("email"):
        if "@" not in msg or "." not in msg:
            state["reply"] = "Please enter a valid email address."
            return state

        state["email"] = msg
        state["reply"] = "Great. Which creator platform do you mainly use?"
        return state

    if not state.get("platform"):
        state["platform"] = msg
        mock_lead_capture(
            state["name"],
            state["email"],
            state["platform"]
        )

        state["mode"] = "done"
        state["reply"] = "Perfect. You're all set — our team will reach out shortly."
        return state

    state["reply"] = "You're already registered."
    return state


def general_node(state: AgentState):
    state["reply"] = "I can help with pricing, plan recommendations, features, or getting started."
    return state

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("greet", greet_node)
    graph.add_node("rag", rag_node)
    graph.add_node("lead", lead_node)
    graph.add_node("collect", collect_node)
    graph.add_node("general", general_node)

    graph.set_conditional_entry_point(router)

    graph.add_edge("greet", END)
    graph.add_edge("rag", END)
    graph.add_edge("lead", END)
    graph.add_edge("collect", END)
    graph.add_edge("general", END)

    return graph.compile()