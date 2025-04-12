import asyncio
import websockets
import json
from shared.protocol import Message, MessageType
import logging
from typing import Dict, Set

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RelayServer:
    def __init__(self):
        self.connected_devices: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.paired_devices: Dict[str, Set[str]] = {}  # device_id -> set of paired device_ids

    async def handle_connection(self, websocket: websockets.WebSocketServerProtocol, path: str):
        device_id = None
        try:
            async for message in websocket:
                message = Message.from_json(message)
                
                if message.type == MessageType.PAIR_REQUEST:
                    device_id = message.data["device_id"]
                    self.connected_devices[device_id] = websocket
                    logger.info(f"Device connected: {device_id}")
                    
                    # Send pairing response
                    response = Message(
                        message_type=MessageType.PAIR_RESPONSE,
                        data={"status": "connected"}
                    )
                    await websocket.send(response.to_json())
                    
                elif message.type == MessageType.CLIPBOARD_UPDATE:
                    if device_id in self.paired_devices:
                        # Forward the message to all paired devices
                        for paired_id in self.paired_devices[device_id]:
                            if paired_id in self.connected_devices:
                                await self.connected_devices[paired_id].send(message.to_json())
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Device disconnected: {device_id}")
        finally:
            if device_id:
                self.connected_devices.pop(device_id, None)
                # Remove from all pairing lists
                for paired_set in self.paired_devices.values():
                    paired_set.discard(device_id)
                self.paired_devices.pop(device_id, None)

    async def start(self, host: str = "localhost", port: int = 8765):
        server = await websockets.serve(self.handle_connection, host, port)
        logger.info(f"Relay server started on ws://{host}:{port}")
        await server.wait_closed()

async def main():
    server = RelayServer()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main()) 