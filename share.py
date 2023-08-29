import numpy as np
import cv2
import pyautogui as pag
import websockets
import threading
import time
import asyncio

data = None
def start_refresh_data():
    def refresh_data():
        global data
        while True:
            frame = pag.screenshot()
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB)
            result, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            data = frame.tobytes()
            time.sleep(0.1)
    threading.Thread(target=refresh_data, daemon=True).start()

async def connect_to_server():
    URL = "ws://stream.kutuptilkisi.dev"
    async with websockets.connect(URL) as websocket:
        await websocket.send("share")
        while True:
            await asyncio.sleep(0.2)
            await websocket.send(data)

if __name__ == "__main__":
    start_refresh_data()
    asyncio.run(connect_to_server())