from aiogram import Bot, Dispatcher, executor, types
import websockets
# import os
# import django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "messanger.settings")
# django.setup()

# Create bot instance

# logging.basicConfig(level=logging.INFO)
bot = Bot(token='5825261092:AAE_GMVgpcTq3S3vhAUwuQ82w2PYdf579A8')

# Create dispatcher
dp = Dispatcher(bot)

# Handle /start command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    group_id = message.chat.id
    await message.answer(f"This message is from group/channel ID: {group_id}")

async def send_message(user_id, text):
    await bot.send_message(chat_id=user_id, text=text)

@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    await connect_websocket(text)

async def connect_websocket(text):
    async with websockets.connect('ws://127.0.0.1:8000/ws/chat/1/') as websocket:
        await websocket.send(text)

# @dp.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup', 'channel'])
# async def handle_group_message(message: types.Message):
#     group_id = message.chat.id
#     await message.answer(f"This message is from group/channel ID: {group_id}")


# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)