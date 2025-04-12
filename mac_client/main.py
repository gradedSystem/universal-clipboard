import asyncio
import websockets
import json
import time
from AppKit import NSPasteboard, NSPasteboardTypeString, NSPasteboardTypePNG
from Foundation import NSData
from shared.encryption import EncryptionManager
from shared.protocol import Message, MessageType, ClipboardData
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MacClipboardClient:
    def __init__(self, server_url: str = "ws://localhost:8765"):
        self.server_url = server_url
        self.device_id = str(uuid.uuid4())
        self.encryption = EncryptionManager()
        self.pasteboard = NSPasteboard.generalPasteboard()
        self.last_clipboard_content = None
        self.websocket = None
        self.is_connected = False

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.server_url)
            self.is_connected = True
            logger.info("Connected to server")
            
            # Send initial pairing request
            await self.send_pair_request()
            
            # Start clipboard monitoring
            asyncio.create_task(self.monitor_clipboard())
            
            # Start message handling
            await self.handle_messages()
            
        except Exception as e:
            logger.error(f"Connection error: {e}")
            self.is_connected = False

    async def send_pair_request(self):
        message = Message(
            message_type=MessageType.PAIR_REQUEST,
            data={
                "device_id": self.device_id,
                "encryption_key": self.encryption.get_key()
            }
        )
        await self.websocket.send(message.to_json())

    async def monitor_clipboard(self):
        while self.is_connected:
            try:
                # Check for text
                text = self.pasteboard.stringForType_(NSPasteboardTypeString)
                if text and text != self.last_clipboard_content:
                    self.last_clipboard_content = text
                    await self.send_clipboard_update(text.encode(), "text/plain")
                
                # Check for image
                image_data = self.pasteboard.dataForType_(NSPasteboardTypePNG)
                if image_data and image_data != self.last_clipboard_content:
                    self.last_clipboard_content = image_data
                    await self.send_clipboard_update(image_data.bytes(), "image/png")
                
                await asyncio.sleep(0.5)
            except Exception as e:
                logger.error(f"Clipboard monitoring error: {e}")

    async def send_clipboard_update(self, content: bytes, content_type: str):
        if not self.is_connected:
            return
            
        clipboard_data = ClipboardData(
            content_type=content_type,
            content=content,
            timestamp=time.time()
        )
        
        encrypted_content = self.encryption.encrypt(content)
        
        message = Message(
            message_type=MessageType.CLIPBOARD_UPDATE,
            data=clipboard_data.to_dict(),
            device_id=self.device_id
        )
        
        await self.websocket.send(message.to_json())

    async def handle_messages(self):
        while self.is_connected:
            try:
                message = await self.websocket.recv()
                message = Message.from_json(message)
                
                if message.type == MessageType.CLIPBOARD_UPDATE:
                    await self.handle_clipboard_update(message)
                elif message.type == MessageType.PAIR_RESPONSE:
                    logger.info("Device paired successfully")
                
            except Exception as e:
                logger.error(f"Message handling error: {e}")
                self.is_connected = False
                break

    async def handle_clipboard_update(self, message: Message):
        try:
            clipboard_data = ClipboardData.from_dict(message.data)
            decrypted_content = self.encryption.decrypt(clipboard_data.content)
            
            if clipboard_data.content_type == "text/plain":
                self.pasteboard.clearContents()
                self.pasteboard.setString_forType_(decrypted_content.decode(), NSPasteboardTypeString)
            elif clipboard_data.content_type == "image/png":
                self.pasteboard.clearContents()
                ns_data = NSData.dataWithBytes_length_(decrypted_content, len(decrypted_content))
                self.pasteboard.setData_forType_(ns_data, NSPasteboardTypePNG)
                
        except Exception as e:
            logger.error(f"Error handling clipboard update: {e}")

async def main():
    client = MacClipboardClient()
    await client.connect()

if __name__ == "__main__":
    asyncio.run(main()) 