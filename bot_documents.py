from aiogram import executor, Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import websockets
import json
import mysql.connector

DEPARTMENT_NAME = 'document'

token = '5877397302:AAGifsgJrKUZR78oGRnysCKmxINHzkYOVnU'
bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def send_message(user_id, text):
    message = await bot.send_message(chat_id=user_id, text=text)
    return message.message_id


async def send_message_via_websocket(message_data):
    async with websockets.connect('ws://127.0.0.1:8765/' + str(message_data['chat'])) as websocket:
        await websocket.send(json.dumps(message_data))
        print(f'Sent message: {message_data["message"]}')

def set_message_data(rep_tgid, chat_id, text, tgid):
    conn = mysql.connector.connect(user='yehor', password='4vRes4^9mH', host='mysqlserver3.mysql.database.azure.com', database='messenger')
    cursor = conn.cursor()

    query = 'SELECT chat_id FROM chats_message WHERE tgid = %s AND driver_id = %s'
    values = (rep_tgid, chat_id)
    cursor.execute(query, values)
    chat = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {'message': text, 'user': '-', 'chat': chat, 'driver': chat_id, 'id': tgid}

@dp.message_handler()
async def handle_message(message: types.Message):
    if message.reply_to_message:
        try:
            response = await send_message_via_websocket(set_message_data(message.reply_to_message.message_id, message.chat.id, message.text, message.message_id))
            print(response)
        except (ConnectionError, websockets.WebSocketException) as e:
            print(f"Error occurred while connecting to websocket: {e}")

if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        pass