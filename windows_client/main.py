import asyncio
import websockets
import json
import time
import win32clipboard
import win32con
import io
from PIL import Image
from shared.encryption import EncryptionManager
from shared.protocol import Message, MessageType, ClipboardData
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WindowsClipboardClient:
    def __init__(self, server_url: str = "ws://localhost:8765"):
        self.server_url = server_url
        self.device_id = str(uuid.uuid4())
        self.encryption = EncryptionManager()
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
                win32clipboard.OpenClipboard()
                
                # Check for text
                if win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
                    text = win32clipboard.GetClipboardData(win32con.CF_TEXT)
                    if text and text != self.last_clipboard_content:
                        self.last_clipboard_content = text
                        await self.send_clipboard_update(text, "text/plain")
                
                # Check for image
                elif win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB):
                    image_data = win32clipboard.GetClipboardData(win32con.CF_DIB)
                    if image_data and image_data != self.last_clipboard_content:
                        self.last_clipboard_content = image_data
                        await self.send_clipboard_update(image_data, "image/png")
                
                win32clipboard.CloseClipboard()
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Clipboard monitoring error: {e}")
                try:
                    win32clipboard.CloseClipboard()
                except:
                    pass

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
            
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            
            if clipboard_data.content_type == "text/plain":
                win32clipboard.SetClipboardText(decrypted_content.decode())
            elif clipboard_data.content_type == "image/png":
                # Convert PNG data to DIB format for Windows clipboard
                image = Image.open(io.BytesIO(decrypted_content))
                output = io.BytesIO()
                image.save(output, format='BMP')
                data = output.getvalue()[14:]  # Remove BMP header
                win32clipboard.SetClipboardData(win32con.CF_DIB, data)
            
            win32clipboard.CloseClipboard()
            
        except Exception as e:
            logger.error(f"Error handling clipboard update: {e}")
            try:
                win32clipboard.CloseClipboard()
            except:
                pass

async def main():
    client = WindowsClipboardClient()
    await client.connect()

if __name__ == "__main__":
    asyncio.run(main()) 