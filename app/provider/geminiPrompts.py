from typing import List
from app.provider.crossProviderPrompts import filter_context_by_tokens

def gemini_genUserQuestion(question: str, token_limit: int, used_tokens: int, context: List[str] | None = None) -> str:
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
