from app.rest.models.EveModels import AIChatMessage
from typing import List

def count_tokens(messages: List[AIChatMessage]) -> int:
    """Estimate the number of tokens in a list of messages.
    This is a rough approximation - on average, 1 token ~= 4 characters in English."""
    total_chars = sum(len(msg.content) + len(msg.role) for msg in messages)
    estimated_tokens = total_chars // 4  # rough approximation
    return estimated_tokens
