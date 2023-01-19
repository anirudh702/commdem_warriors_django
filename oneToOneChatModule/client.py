import asyncio
import websockets
import aioconsole


async def received_message_handler(websocket):
    while True:
        message = await websocket.recv()
        await aioconsole.aprint(message)


async def sent_message_handler(websocket):
    while True:
        message = await aioconsole.ainput()
        await websocket.send(message)


async def main():
    uri = "ws://localhost:8001"
    print("You can now chat with other people in the room!")

    async with websockets.connect(uri) as websocket:
        await asyncio.gather(
            received_message_handler(websocket),
            sent_message_handler(websocket)
        )

asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop.run_forever()

 

asyncio.get_event_loop().run_until_complete(main())

asyncio.get_event_loop.run_forever()