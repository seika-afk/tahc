import asyncio
import websockets

clients = []
fastest_time = None

async def handle_message(websocket):
    global clients, fastest_time
    try:
        message = await websocket.recv()

        if message == "b":
            response_time = asyncio.get_event_loop().time()
            clients.append([websocket, response_time])

            if len(clients) == 1:
                await websocket.send("first place")
                fastest_time = response_time
            else:
                t = round(response_time - fastest_time, 2)
                await websocket.send(f"2nd place time: {t}")

    except websockets.ConnectionClosed:
        print("Client disconnected")

async def start_server():
    async with websockets.serve(handle_message, "localhost", 8765):
        print("Server started")
        await asyncio.Future()  # run forever

asyncio.run(start_server())

