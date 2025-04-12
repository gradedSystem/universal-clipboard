import pytest
from shared.protocol import Message, MessageType, ClipboardData
import json
import time

def test_message_serialization():
    # Test message serialization/deserialization
    original_message = Message(
        message_type=MessageType.CLIPBOARD_UPDATE,
        data={"test": "data"},
        device_id="test_device"
    )
    
    json_str = original_message.to_json()
    deserialized_message = Message.from_json(json_str)
    
    assert deserialized_message.type == original_message.type
    assert deserialized_message.data == original_message.data
    assert deserialized_message.device_id == original_message.device_id

def test_clipboard_data():
    # Test clipboard data serialization/deserialization
    content = b"Test content"
    timestamp = time.time()
    
    clipboard_data = ClipboardData(
        content_type="text/plain",
        content=content,
        timestamp=timestamp
    )
    
    data_dict = clipboard_data.to_dict()
    deserialized_data = ClipboardData.from_dict(data_dict)
    
    assert deserialized_data.content_type == clipboard_data.content_type
    assert deserialized_data.content == clipboard_data.content
    assert deserialized_data.timestamp == clipboard_data.timestamp

def test_message_types():
    # Test all message types
    for message_type in MessageType:
        message = Message(
            message_type=message_type,
            data={"test": "data"}
        )
        json_str = message.to_json()
        deserialized = Message.from_json(json_str)
        assert deserialized.type == message_type 