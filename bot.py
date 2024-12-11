import PIL.Image
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import BufferedInputFile

from io import BytesIO
import PIL

import asyncio

import api

API_TOKEN = 'token'

GROUPS = ['1.1', '1.2', '2.1', '2.2', '3.1', '3.2']

bot = Bot(token=API_TOKEN)
router = Router()
dp = Dispatcher()
dp.include_router(router)

@dp.message(Command("start"))
async def send_welcome(message: types.Message, command: CommandStart):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id, text='123')

@dp.message(Command("get_image"))
async def get_schedule_image(message: types.Message, command: CommandStart):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id, text="Fetching a grafic...")
    image_url = api.get_image_url()
    image: PIL.Image = api.get_image_by_url(image_url)

    await bot.send_photo(chat_id=user_id, photo=BufferedInputFile(BytesIO(image).read()))

@dp.message(Command("get"))
async def get_schedule_image(message: types.Message, command: CommandStart):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id, text="Пошук... (не жми сто раз)")
    offs_timelines = api.get_offs_timelines()

    msg = ''

    if offs_timelines:
        msg += 'Йоу. Осьо коли в твоїй групі (1.1) вимикатимуть світло:\n'
        for timeline in offs_timelines:
            off_start, off_end = timeline
            off_start = off_start if off_start > 9 else f"0{off_start}"
            off_end = off_end if off_end > 9 else f"0{off_end}"

            msg += f'- {off_start}:00 - {off_end}:00\n'
    else:
        msg += "Везунчик, вдавись тим світлом (без вимкнень)"

    await bot.send_message(chat_id=user_id, text=msg)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
