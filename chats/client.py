import websockets
import ssl
import json

ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def set_message_data(chat_id, text, department, user) -> dict:
    return {'message': text, 'user': user, 'chat': chat_id, 'department': department, 'typeOfMessage': 'text', 'close':True}

async def send_message_via_websocket(message_data: dict):
    print("CONNECTED")
    async with websockets.connect('wss://entinsoft.com:8080/' + str(message_data['chat']), ssl=ssl_context) as websocket:
        await websocket.send(json.dumps(message_data))
        try:
            while True:
                await websocket.recv()
        except:
            print(f'Sent message: {message_data["message"]}')
    print("DISC")