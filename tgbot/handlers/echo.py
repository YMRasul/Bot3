from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import logger

async def bot_echo_all(message: types.Message, state: FSMContext):
    logger.info(f"{message.from_user.id}  Noma'lum komanda berildi. {message.text}")
    await message.answer("Noma'lum komanda berildi." )


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
