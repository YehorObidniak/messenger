from aiogram import executor, Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import websockets
import pymysql
import json

conn = pymysql.connect(
    host='mysqlserver3.mysql.database.azure.com',
    user='yehor',
    password='4vRes4^9mH',
    database='messenger'
)
cursor = conn.cursor()
# cursor.execute("USE messenger")
# cursor.execute("INSERT INTO chats_issue(id, title, description, priority, status, startTime, time, endTime, department) VALUES (1, 'test issue', 'i fell out of my bed mazafaka', 2, 'in process', 1212, 34324, 1212, 'documents');")
# conn.commit()
member_info = []

token = '5825261092:AAE_GMVgpcTq3S3vhAUwuQ82w2PYdf579A8'
bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def send_message(user_id, text):
    await bot.send_message(chat_id=user_id, text=text)

async def send_message_via_websocket(message_data):
    async with websockets.connect('ws://127.0.0.1:8765') as websocket:
        await websocket.send(json.dumps(message_data))
        print(f'Sent message: {message_data["message"]}')

@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    print(message.from_user.username + ": " + message.text)
    # await state.set_state('waiting_for_login')
    await message.answer(text="hello")
    await message.answer(text="Здравейте\nВведите свой логин:")

@dp.message_handler()
async def handle_message(message: types.Message):
    message_data = {
        'message': message.text,
        'user': '-',
        'chat': 1,
        'driver': message.from_user.id
    }
    try:
        response = await send_message_via_websocket(message_data)
        print(response)
    except (ConnectionError, websockets.WebSocketException) as e:
        print(f"Error occurred while connecting to websocket: {e}")

@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def user_joined_chat(message: types.Message, state: FSMContext):
    print(f'User {message.from_user.username} added')
    await state.set_state('waiting_for_login')
    await message.answer(text="Здравейте\nВведите свой логин:")

@dp.message_handler(content_types = [types.ContentType.TEXT], state = "waiting_for_login")
async def login_input(message: types.Message, state: FSMContext):
    print(message.from_user.username+": "+ message.text)
    cursor.execute("SELECT * FROM chats_users WHERE email = %s",(message.text,))
    if cursor.fetchall():
        member_info.append(message.text)
        await state.set_state('waiting_for_password')
        await message.answer(text="Введите пароль:")
    else:
        await state.set_state('waiting_for_login')
        await message.answer(text="Такого пользователя не существует\nВведите логин еще раз:")


@dp.message_handler(content_types = [types.ContentType.TEXT], state = "waiting_for_password")
async def password_input(message: types.Message, state: FSMContext):
    print(message.from_user.username+": "+ message.text)
    cursor.execute("SELECT * FROM chats_users WHERE email = %s AND password = %s",(member_info[0], message.text,))
    if cursor.fetchall():
        member_info.append(message.text)
        await state.finish()
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="садись прокачу", url="https://www.youtube.com/watch?v=nx3A-YmfFHw&ab_channel=%D0%91%D0%B0%D0%BB%D0%B1%D0%B5%D1%81%D1%8B"))
        await message.answer(text="Вы прошли проверку, подздравляем!", reply_markup=markup)
    else:
        await state.set_state('waiting_for_password')
        await message.answer(text="Вы ввели неверный пароль, попробуйте еще раз:")




if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        # Закрытие соединения с базой данных
        conn.close()