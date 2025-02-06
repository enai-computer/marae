from .appletModels import ToolDefinition
import asyncio

PREDEFINED_APPLETS = [
    "https://applets.unternet.co/maps",
    "https://applets.unternet.co/calculator",
    "https://applets.unternet.co/weather",
    "https://applets.unternet.co/todo"
    ]

gAppletManager = None

async def init_applet_manager():
    print("starting to initialize applet manager")
    global gAppletManager
    gAppletManager = AppletManager()
    await gAppletManager.initialize()

class AppletManager:
    """
    Manages applets and provides them as tools to the LLMs.
    """
    def __init__(self):
        self.applets = []
        self.openAI_tools = []
        self.loaded = False

    async def initialize(self):
        print("init on applet manager called")
        if self.loaded:
            return
        for applet_url in PREDEFINED_APPLETS:
            try:
                print(f"loading applet from {applet_url}")
                self.applets.append(await ToolDefinition.load_from_url(applet_url))
            except Exception as e:
                print(f"error loading applet from {applet_url}: {e}")
                continue

        for applet in self.applets:
            self.openAI_tools.append(applet.to_openai_tool_definition())
        print(self.openAI_tools)
        self.loaded = True
