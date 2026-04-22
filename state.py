from typing import TypedDict, Optional, List

class AgentState(TypedDict, total=False):
    user_input: str
    reply: str
    messages: List[str]
    intent: str
    mode: str
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]