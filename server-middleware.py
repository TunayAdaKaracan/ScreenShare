import websockets
import asyncio
import pathlib
import ssl

CONNECTIONS = []
image_data = None

async def broadcast(data):
    for connection in CONNECTIONS:
        await connection.send(data)

async def sharer_client(websocket):
    global image_data
    while True:
        image_data = await websocket.recv()
        

async def client_connection(websocket):
    type_websocket = await websocket.recv()

    if type_websocket == "share":
        await sharer_client(websocket)
    elif type_websocket == "browser":
        CONNECTIONS.append(websocket)
        await websocket.wait_closed()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_certf = pathlib.Path(__file__).with_name("cert.pem")
ssl_key = pathlib.Path(__file__).with_name("private-key.pem")
ssl_context.load_cert_chain(certfile=ssl_certf, keyfile=ssl_key)

async def main():
    async with websockets.serve(client_connection, "localhost", 8080, ssl=ssl_context):
        while True:
            await broadcast(image_data)
            await asyncio.sleep(0.2)

if __name__ == "__main__":
    asyncio.run(main())