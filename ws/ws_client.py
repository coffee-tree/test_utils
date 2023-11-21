import asyncio
import websockets
import json


async def client():
    uri = "ws://43.201.20.124:6789"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"receive data: {message}")


asyncio.get_event_loop().run_until_complete(client())
