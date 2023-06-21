import asyncio
from websockets.server import serve
import websockets
import json
import bot_documents
import messenger.chats.bot_sales as bot_sales
import mysql.connector
import ssl
import os
from messenger.chats.db_manager import DBManager

script_dir = os.path.dirname(os.path.abspath(__file__))
cert = os.path.join(script_dir, "entinsoft.crt")
key = os.path.join(script_dir, "entinsoft.key")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(cert, key)

names = {'Бухгалтерия':bot_documents, 'CarsHauler':bot_sales}

class Producer:
    def __init__(self) -> None:
        self.bots = {}
        self.clients = {}
        self.dbManager = DBManager()

    async def send_message(self, message, path):
        for client in self.clients[path]:
            await client.send(message)

    async def handle_message(self, websocket, path):
        tgid = None
        data = await websocket.recv()
        
        print("client send:", data)
        message = json.loads(data)
        try:
            if message['user'] != '-':
                tgid = await names[message['department']].send_message(message['chat'], message['message'])
        except:
            print("Error")
        await self.send_message(json.dumps(message), path)
        if 'id' in message:
            tgid = message['id']

        print(f"ID: {tgid}")
        self.dbManager.insert_message(tgid, message['user'], message['message'], int(message['chat']), message['department'])
        

    async def new_client_connected(self, websocket, path:str):
        print("New client")
        print(path)
        if path in self.clients:
            self.clients[path].append(websocket)
        else:
            self.clients[path] = []
            self.clients[path].append(websocket)

        try:
            while True:
                await self.handle_message(websocket, path)

        except websockets.exceptions.ConnectionClosed:
            self.clients[path].remove(websocket)
            print("Goodbye!")

    async def main(self):
        async with serve(self.new_client_connected, "0.0.0.0", 8080, ssl=ssl_context):
            print('CoNnected')
            await asyncio.Future()

pr = Producer()
asyncio.run(pr.main())
