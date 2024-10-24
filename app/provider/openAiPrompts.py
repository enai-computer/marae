from typing import List

def get_usr_prompt_space_name(space_name: str) -> str:
    return f"""
        Enai is an interpersonal computer
        optimized for AI and the net.
        (It is a browser OS, emphasis on OS)

        By organizing your whole computer
        around your intent, Enai helps you be
        calmer, smarter, and more effective.

        How to use Enai:
        First you set your intent, which creates a space for you to practice that intent.

        In the space, you can

        - Surf the web
        - Right click to pin websites to the menu bar to access them like apps
        - Create and name groups so that you can be organized
        - Write notes or paste text on the canvas
        - Chat with Enai (as an AI tool) about one or more specific tabs

        Once you are finished working on a particular topic, you can create or reopen another space and Enai saves all your work. So you can work on your first intent, put it away, and come back later. If you’re using your computer to do something complicated for more than a few days, Enai can help you keep all that information organized and easily accessible.
        Generate a welcome text for a new space called {space_name} with a maximum of 100 words.
    """

def get_usr_prompt_space_name_group_name(space_name: str, group_name: str) -> str:
    return f"""
        Give me one insightful sentence about "{space_name}" and "{group_name}" assuming i'm very intelligent and using simple language.
    """

def get_usr_prompt_space_name_group_name_context_tabs(space_name: str, group_name: str, context_tabs: List[str]) -> str:
    return f"""
        Give me one insightful sentence about "{space_name}" and "{group_name}" and the following tabs: {context_tabs} assuming i'm very intelligent and using simple language.
    """

def get_usr_prompt_space_name_context_tabs(space_name: str, context_tabs: List[str]) -> str:
    return f"""
        Give me one insightful sentence about "{space_name}" and the following tabs: {context_tabs} assuming i'm very intelligent and using simple language.
    """
