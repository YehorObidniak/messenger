import asyncio
from websockets.server import serve
from websockets.sync.client import connect
import websockets
import json
import bot_documents
import bot_sales
import pymysql

conn = pymysql.connect(
    host='mysqlserver3.mysql.database.azure.com',
    user='yehor',
    password='4vRes4^9mH',
    database='messenger'
)
cursor = conn.cursor()

names = {'Бухгалтерия':bot_documents, 'CarsHauler':bot_sales}

class Producer:
    def __init__(self) -> None:
        self.bots = {}
        self.clients = {}

    async def send_message(self, message, path):
        for client in self.clients[path]:
            await client.send(message)

    async def handle_message(self, websocket, path):
        data = await websocket.recv()
        print("client send:", data)
        message = json.loads(data)
        try:
            if message['user'] != '-':
                await self.bots[path].send_message(message['driver'], message['message'])
        except:
            print("Error")
        await self.send_message(json.dumps(message), path)
        print('sended')
        insertion = 'INSERT INTO chats_message(from_user, text, chat_id, driver_id) VALUES(%s, %s, %s, %s)'
        values = (message['user'], message['message'], int(message['chat']), int(message['driver']))
        cursor.execute(insertion, values)
        conn.commit()
        print('saved')

    async def new_client_connected(self, websocket, path:str):
        print("New client")
        print(path)
        if path in self.clients:
            self.clients[path].append(websocket)
        else:
            self.clients[path] = []
            self.clients[path].append(websocket)

        if path not in self.bots:
            cursor.execute(f"SELECT department_id FROM chats_chat WHERE id = '{path.replace('/', '')}'")
            id = cursor.fetchone()[0]
            cursor.execute(f"SELECT name FROM chats_department WHERE id = '{id}'")
            name = cursor.fetchone()[0]
            print(name)
            self.bots[path] = names[name]

        try:
            while True:
                await self.handle_message(websocket, path)

        except websockets.exceptions.ConnectionClosed:
            self.clients[path].remove(websocket)
            print("Goodbye!")

    async def main(self):
        async with serve(self.new_client_connected, "localhost", 8765):
            print('CoNnected')
            await asyncio.Future()

pr = Producer()
asyncio.run(pr.main())