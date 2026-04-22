from typing import TypedDict, Optional


class ChatState(TypedDict, total=False):
    intent: str
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]
    qualified: bool