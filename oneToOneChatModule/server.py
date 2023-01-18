# import asyncio
# import websockets

# async def hello(websocket, path):
#     name = await websocket.recv()
#     print("< {}".format(name))

#     greeting = "Hello {}!".format(name)
#     await websocket.send(greeting)
#     print("> {}".format(greeting))

# start_server = websockets.serve(hello, 'localhost', 8765)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

from aiohttp import web
import socketio

## creates a new Async Socket IO Server
sio = socketio.AsyncServer()
## Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
## instance
sio.attach(app)

## we can define aiohttp endpoints just as we normally
## would with no change

## If we wanted to create a new websocket endpoint,
## use this decorator, passing in the name of the
## event we wish to listen out for
@sio.on('message')
async def print_message(sid, message):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: " , sid)
    print(message)

## We bind our aiohttp endpoint to our app
## router
# app.router.add_get('/', index)

## We kick off our server
if __name__ == '__main__':
    web.run_app(app)