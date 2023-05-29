from aiogram import executor, Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import websockets
import pymysql
import json

DEPARTMENT_NAME = 'document'

conn = pymysql.connect(
    host='mysqlserver3.mysql.database.azure.com',
    user='yehor',
    password='4vRes4^9mH',
    database='messenger'
)

cursor = conn.cursor()

token = '5877397302:AAGifsgJrKUZR78oGRnysCKmxINHzkYOVnU'
bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def send_message(user_id, text):
    await bot.send_message(chat_id=user_id, text=text)

async def send_message_via_websocket(message_data):
    async with websockets.connect('ws://127.0.0.1:8765/' + str(message_data['chat'])) as websocket:
        await websocket.send(json.dumps(message_data))
        print(f'Sent message: {message_data["message"]}')

@dp.message_handler()
async def handle_message(message: types.Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
        print(text)
        cursor.execute(f"SELECT from_user FROM chats_message WHERE text = '{text}'")
        id = cursor.fetchone()[0]
        cursor.execute(f"SELECT id FROM chats_chat WHERE driver_id = '{message.chat.id}' AND user_id='{id}'")
        chat = cursor.fetchone()[0]
        message_data = {
            'message': message.text,
            'user': '-',
            'chat': chat,
            'driver': message.chat.id
        }
        try:
            response = await send_message_via_websocket(message_data)
            print(response)
        except (ConnectionError, websockets.WebSocketException) as e:
            print(f"Error occurred while connecting to websocket: {e}")

if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        # Закрытие соединения с базой данных
        conn.close()