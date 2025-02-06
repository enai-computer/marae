from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import enum

class ToolType(enum.Enum):
    UNTERNET_APPLET = 'unternet-applet'
    UNTERNET_RESOURCE = 'unternet-resource'

@dataclass
class ActionDefinition:
    id: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

    def __init__(self, id: str, description: Optional[str] = None, parameters: Optional[Dict[str, Any]] = None, **kwargs):
      self.id = id
      self.description = description
      self.parameters = parameters

@dataclass
class ManifestIcon:
    src: str
    purpose: Optional[str] = None
    sizes: Optional[str] = None
    type: Optional[str] = None

@dataclass
class ToolDefinition:
    type: ToolType
    url: str
    name: Optional[str] = None
    short_name: Optional[str] = None
    icons: Optional[List[ManifestIcon]] = None
    description: Optional[str] = None
    actions: Optional[List[ActionDefinition]] = None
    
    @classmethod
    async def load_from_url(cls, url: str) -> 'ToolDefinition':
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url + "/manifest.json") as response:
                response.raise_for_status()
                manifest = await response.json()
        
        # Convert icons list if present
        icons = None
        if 'icons' in manifest:
            icons = [ManifestIcon(**icon) for icon in manifest['icons']]
        
        # Convert actions list if present
        actions = None
        if 'actions' in manifest:
            actions = [ActionDefinition(**action) for action in manifest['actions']]
        
        tool_type = ToolType.UNTERNET_APPLET if 'actions' in manifest else ToolType.UNTERNET_RESOURCE

        return cls(
            type=tool_type,
            url=url,
            name=manifest.get('name'),
            short_name=manifest.get('short_name'),
            icons=icons,
            description=manifest.get('description'),
            actions=actions
        )
    
    def to_openai_tool_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.actions,
            }
        }

# Example manifest:
# {
#     "name": "Maps",
#     "short_name": "Maps",
#     "description": "Search for and display locations on a map. Map data can contain: descriptions of places & businesses, reviews, opening hours, etc.",
#     "icons": [
#     {
#       "src": "icon-128x128.png"
#     }
#   ],
#   "actions": [
#     {
#       "id": "search",
#       "description": "Search for locations with Google Maps",
#       "parameters": {
#         "type": "object",
#         "properties": {
#           "query": {
#             "type": "string",
#             "description": "The search query for locations on the map."
#           }
#         },
#         "required": [
#           "query"
#         ]
#       }
#     }
#   ]
# }