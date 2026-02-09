import asyncio
import websockets
import json
import os
from websockets.exceptions import InvalidHandshake

passwd = "0909"
connected_clients = {}  

async def tahc(websocket):
    try:
        box = await websocket.recv()
        name, pwd = box.split(",")

        if pwd != passwd:
            await websocket.send("Wrong Passcode")
            return

        if len(connected_clients) >= 2:
            await websocket.send("Members are Full")
            return

        connected_clients[websocket] = name
        print(f"User {name} entered")
        join_msg = json.dumps({"system": f"{name} joined"})
        await asyncio.gather(*[ws.send(join_msg) for ws in connected_clients])

        # send current users to the new user
        await websocket.send(json.dumps({"users": list(connected_clients.values())}))

        ######################################### MAIN CHAT LOOP
        while True:
            msg = await websocket.recv()
            broadcast = json.dumps({"from": name, "msg": msg})
            await asyncio.gather(*[
                ws.send(broadcast) for ws in connected_clients if ws != websocket
            ])
    except websockets.ConnectionClosed:
        print(f"{connected_clients.get(websocket, 'Unknown')} disconnected")
    finally:
        if websocket in connected_clients:
            leave_name = connected_clients.pop(websocket)
            leave_msg = json.dumps({"system": f"{leave_name} left"})
            await asyncio.gather(*[ws.send(leave_msg) for ws in connected_clients])

async def starttahc():
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(tahc, "0.0.0.0", port):
        print(f"SERVER STARTED on port {port}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(starttahc())
    except InvalidHandshake:
        print("Ignored non-WebSocket request")
