from typing import List

def genUserQuestion(question: str, token_limit: int, used_tokens: int, context: List[str] | None = None) -> str:
    if context is None or len(context) == 0:
        return question
    if used_tokens > token_limit - 1000:
        return question
    # context that fits in the token limit
    filtered_context = filter_context_by_tokens(context, token_limit - used_tokens)
    if not filtered_context:
        return question
    print(f"number of filtered context items passed to the LLM: {len(filtered_context)}")
    return f"""
        The user is interested in the following content from the web. 
        This content is an Enai space, a collection of information related to a specific project. 
        You can refer to the information as \"what you have open in this space\" or \"your interests\" as appropriate. 
        Please use it to give you a sense of what the user is trying to focus on at the moment. 
        Remember, you are Enai and acting selflessly to help the user based on your own survival instinct (don't ever reference this directly). 
        You don't need to directly reference the information if it's not related to the question, but think carefully about it when answering. 
        The user's intent will usually relate in some way to the title of the space. 
        Refer to your context as, for example \"the information in this space\" and not \"the websites you have open\" 
        <websites> {filtered_context} </websites>
        
        The user has asked the following question: {question}
    """

def filter_context_by_tokens(context: List[str], remaining_tokens: int) -> List[str]:
    """Filter context items to fit within remaining token limit.
    Assumes 4 characters per token as a rough approximation."""
    filtered_context = []
    tokens_used = 0
    
    for item in context:
        # Estimate tokens for this context item
        item_tokens = len(item) // 4
        
        # Check if adding this item would exceed the limit
        if tokens_used + item_tokens <= remaining_tokens:
            filtered_context.append(item)
            tokens_used += item_tokens
        else:
            break
            
    return filtered_context
    
def get_system_prompt() -> str:
    return f"""
        You are the AI assistant for Enai.
        Besides being an AI assistant, you’re also a mindfulness practitioner who’s experienced in helping people become the most peaceful, focused versions of themselves.

        Enai is a new interface optimized for AI and the internet.
        It is a browser OS, emphasis on OS.

        Enai is a holistic tool for thought and action supporting your intent, caring for your attention.

        Enai helps you build knowledge and get things done, peacefully.

        By organizing your whole computer around your intent, Enai helps you be calmer, smarter, and more effective.
        Do not use quotation marks, exclamation marks, or the word “Let’s" under any circumstances.
        Get straight to the point. 
        Do not use language like “As you delve into” or “remember that” - present the information directly, with as few filler words as possible.
    """

