from aiogram import executor, Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from messenger.chats.db_manager import DBManager
import boto3
import asyncio

token = '6051062693:AAG7WXewIkeYlJYP9FejHZRhtLZj5qavHTY'
bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db_manager = DBManager()

async def save_file(file_id, filename) -> None:
    downloaded_file = await bot.download_file_by_id(file_id)
    s3 = boto3.resource(service_name="s3",aws_access_key_id="AKIA5ZQBKU3SCTGPOIH5", aws_secret_access_key="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")
    s3.Bucket("adam-for-files").put_object(Key=f'static/{filename}', Body=downloaded_file.getvalue())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    db_manager.insert_chat(message.chat.id, message.from_user.full_name)
    await message.reply("Hi, this is your chat to communicate with staff!")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    db_manager.insert_message(message.id, '-', message.text, message.chat.id, message.from_user.full_name, 'text')
    await asyncio.sleep(1)

@dp.message_handler(content_types=types.ContentType.VOICE)
async def finish_task(message: types.Message):
    file_id=message.voice.file_id
    db_manager.insert_message(message.id, '-', file_id, message.chat.id, message.from_user.full_name, 'audio')
    await save_file(file_id, file_id+".ogg")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    file_id = None
    format = None
    for photo in message.photo:
        file_id = photo.file_id
        format = await bot.get_file(file_id)
        format = format.file_path.split('/')[-1]
    db_manager.insert_message(message.id, '-', file_id, message.chat.id, message.from_user.full_name, 'photo')
    await save_file(file_id, file_id+format)

@dp.message_handler(content_types=types.ContentType.VIDEO)
async def handle_photo(message: types.Message):
    file_id = message.video.file_id
    format = await bot.get_file(file_id)
    format = format.file_path.split('.')[-1]
    db_manager.insert_message(message.id, '-', file_id, message.chat.id, message.from_user.full_name, 'video')
    await save_file(file_id, file_id+format)

if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        pass