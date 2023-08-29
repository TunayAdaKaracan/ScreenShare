import websockets
import asyncio
import certifi
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
    print("New client")
    type_websocket = await websocket.recv()

    if type_websocket == "share":
        await sharer_client(websocket)
    elif type_websocket == "browser":
        CONNECTIONS.append(websocket)
        await websocket.wait_closed()

ssl_context = ssl.create_default_context(ssl.PROTOCOL_TLS, cafile=certifi.where())
ssl_context.load_cert_chain(certfile=pathlib.Path("./cert.pem"), keyfile=pathlib.Path("./cert-key.pem"), )

async def main():
    async with websockets.serve(client_connection, "0.0.0.0", 8080, ssl=ss):
        while True:
            await broadcast(image_data)
            await asyncio.sleep(0.2)

if __name__ == "__main__":
    asyncio.run(main())