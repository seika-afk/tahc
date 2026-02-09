import asyncio
import websockets

async def start_client():
    async with websockets.connect("ws://localhost:8765") as websocket:
        print("Welcome! Press ENTER to send 'b'...")

        # Wait for user input
        input("> ")
        await websocket.send("b")

        # Receive server response
        message = await websocket.recv()
        print(f"Server says: {message}")

asyncio.run(start_client())

