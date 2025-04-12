import json
from enum import Enum
from typing import Dict, Any, Optional
import base64

class MessageType(Enum):
    CLIPBOARD_UPDATE = "clipboard_update"
    PAIR_REQUEST = "pair_request"
    PAIR_RESPONSE = "pair_response"
    ERROR = "error"
    PING = "ping"
    PONG = "pong"

class Message:
    def __init__(self, message_type: MessageType, data: Dict[str, Any], device_id: Optional[str] = None):
        self.type = message_type
        self.data = data
        self.device_id = device_id

    def to_json(self) -> str:
        return json.dumps({
            "type": self.type.value,
            "data": self.data,
            "device_id": self.device_id
        })

    @classmethod
    def from_json(cls, json_str: str) -> 'Message':
        data = json.loads(json_str)
        return cls(
            message_type=MessageType(data["type"]),
            data=data["data"],
            device_id=data.get("device_id")
        )

class ClipboardData:
    def __init__(self, content_type: str, content: bytes, timestamp: float):
        self.content_type = content_type
        self.content = content
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content_type": self.content_type,
            "content": base64.b64encode(self.content).decode(),
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClipboardData':
        return cls(
            content_type=data["content_type"],
            content=base64.b64decode(data["content"]),
            timestamp=data["timestamp"]
        ) 