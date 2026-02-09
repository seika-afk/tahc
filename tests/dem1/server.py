
import asyncio 
import websockets

async def getOTP(websocket):
    name=await websocket.recv()
    print("Sending OTP of username : ",name)

    greeting=f"{name}: 1245"

    await websocket.send(greeting)
    print(f'server sent : {greeting}')

async def main():
    async with websockets.serve(getOTP,"localhost",8765):
        await asyncio.Future() # run forever



asyncio.run(main())


    
