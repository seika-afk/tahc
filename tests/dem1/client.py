import asyncio
import websockets


async def hello():
    uri="ws://localhost:8765"

    async with websockets.connect(uri) as websocket:
        name=input("> ")
        await websocket.send(name)
        print(f'Client sent :{name}')
        

        greeting=await websocket.recv()

        print(f"client recieved :{greeting}")
asyncio.run(hello())
