import asyncio
import websockets
import json
from datetime import datetime

def ts():
    return datetime.now().strftime("%H:%M:%S")

async def send_message(ws):
    loop = asyncio.get_event_loop()
    while True:
        msg = await loop.run_in_executor(None, input, "> ")
        if msg.lower() == "q":
            print("Exiting chat...")
            await ws.close()
            break
        await ws.send(msg)
        print(f"[{ts()}] You: {msg}")

async def receive_messages(ws):
    try:
        while True:
            msg = await ws.recv()
            try:
                data = json.loads(msg)
                if "msg" in data:
                    print(f"\n[{ts()}] {data['from']}: {data['msg']}")
                elif "system" in data:
                    print(f"\n[{ts()}] [System] {data['system']}")
                elif "users" in data:
                    print(f"\n[{ts()}] Users: {', '.join(data['users'])}")
            except:
                print(f"\n{msg}")
            print("> ", end="", flush=True)
    except websockets.ConnectionClosed:
        print("\n[System] Server closed connection")

async def main():
    print("Welcome to TahC CLI Chat...")
    await asyncio.sleep(0.1)

    name = input("Enter your name: ")
    pwd = input("Enter Passcode: ")
    comp = f"{name},{pwd}"

    async with websockets.connect("ws://localhost:8765") as ws:
        await ws.send(comp)
        first_msg = await ws.recv()
        try:
            data = json.loads(first_msg)
            if "system" in data:
                print(f"[System] {data['system']}")
            if "users" in data:
                print(f"Current users: {', '.join(data['users'])}")
        except:
            print(first_msg)

        await asyncio.gather(
            send_message(ws),
            receive_messages(ws)
        )

asyncio.run(main())

