import numpy as np
import cv2
import pyautogui as pag
import asyncio
import websockets
import threading
import pathlib
import time

data = None
def refresh_data():
    global data
    while True:
        frame = pag.screenshot()
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB)
        result, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        data = frame.tobytes()
        time.sleep(0.4)
	
threading.Thread(target=refresh_data, daemon=True).start()

async def hello(websocket):
    while True:
        await websocket.send(data)
        await asyncio.sleep(0.1)

async def main():
    async with websockets.serve(hello, "localhost", 8080):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    print("Starting Server")
    asyncio.run(main())