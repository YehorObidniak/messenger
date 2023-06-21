from aiogram import executor, Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import websockets
import json
import mysql.connector
import ssl
from messenger.chats.db_manager import DBManager
import boto3

ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

DEPARTMENT_NAME = 'document'

token = '5877397302:AAGifsgJrKUZR78oGRnysCKmxINHzkYOVnU'
bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db_manager = DBManager()

async def send_message(user_id, text):
    message = await bot.send_message(chat_id=user_id, text=text)
    return message.message_id

async def save_audio(file_id) -> None:
    downloaded_file = await bot.download_file_by_id(file_id)
    s3 = boto3.resource(service_name="s3",aws_access_key_id="AKIA5ZQBKU3SCTGPOIH5", aws_secret_access_key="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")
    s3.Bucket("adam-for-files").put_object(Key=f'{file_id}.ogg', Body=downloaded_file.getvalue())

async def send_message_via_websocket(message_data: dict):
    async with websockets.connect('wss://entinsoft.com:8080/' + str(message_data['chat']), ssl=ssl_context) as websocket:
        await websocket.send(json.dumps(message_data))
        print(f'Sent message: {message_data["message"]}')

def set_message_data(chat_id, text, tgid, name, audioName) -> dict:
    return {'message': text, 'user': '-', 'chat': chat_id, 'driver': chat_id, 'id': tgid, 'department': name, 'audioName':audioName}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    db_manager.insert_chat(message.chat.id, message.from_user.full_name)
    await message.reply("Hi, this is your chat to communicate with staff!")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    try:
        response = await send_message_via_websocket(set_message_data(message.chat.id, message.text, message.message_id, message.from_user.full_name))
        print(response)
    except (ConnectionError, websockets.WebSocketException) as e:
        print(f"Error occurred while connecting to websocket: {e}")


@dp.message_handler(content_types=types.ContentType.VOICE)
async def finish_task(message: types.Message):
    file_id=message.voice.file_id
    await save_audio(file_id)

    try:
        response = await send_message_via_websocket(set_message_data(message.chat.id, 'None', message.message_id, message.from_user.full_name, file_id))
        print(response)
    except (ConnectionError, websockets.WebSocketException) as e:
        print(f"Error occurred while connecting to websocket: {e}")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    file_id = None
    filename = None
    for photo in message.photo:
        file_id = photo.file_id
        filename = await bot.get_file(file_id)
        filename = filename.file_path.split('/')[-1]
    downloaded_file = await bot.download_file_by_id(file_id)
    print(downloaded_file)
    s3 = boto3.resource(service_name="s3",aws_access_key_id="AKIA5ZQBKU3SCTGPOIH5", aws_secret_access_key="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")
    s3.Bucket("adam-for-files").put_object(Key=f'{file_id}', Body=downloaded_file.getvalue())

    try:
        response = await send_message_via_websocket(set_message_data(message.chat.id, filename, message.message_id, message.from_user.full_name, 'photo'))
        print(response)
    except (ConnectionError, websockets.WebSocketException) as e:
        print(f"Error occurred while connecting to websocket: {e}")

@dp.message_handler(content_types=types.ContentType.VIDEO)
async def handle_photo(message: types.Message):
    file_id = message.video.file_id
    format = await bot.get_file(file_id)
    format = format.file_path.split('.')[-1]
    downloaded_file = await bot.download_file_by_id(file_id)
    print(downloaded_file)
    s3 = boto3.resource(service_name="s3",aws_access_key_id="AKIA5ZQBKU3SCTGPOIH5", aws_secret_access_key="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")
    s3.Bucket("adam-for-files").put_object(Key=f'static/{file_id}.{format}', Body=downloaded_file.getvalue())

    try:
        response = await send_message_via_websocket(set_message_data(message.chat.id, file_id+"."+format, message.message_id, message.from_user.full_name, 'video'))
        print(response)
    except (ConnectionError, websockets.WebSocketException) as e:
        print(f"Error occurred while connecting to websocket: {e}")

if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        pass
