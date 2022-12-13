from aiogram import Dispatcher,types
from aiogram.types import Message
from create_bot import bot
from .user import rootpath

#@dp.message_handler(commands=["start"], state="*", is_admin=True)
async def admin_start(message: Message):
    await message.answer("Скрепки ни босинг !\n Fayl   'NNNNNNNNN_gggg_mm.xls'  ko'rinishida bo'lishi kerak\n Misol 200918719_2022_11.xls")

#@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def scan_doc(message: types.document):
    try:
        chat_id = message.chat.id
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)

        fil = rootpath() + '\\files\\'  # отвратительное решение
        src = fil + message.document.file_name
        print("Сохранен как "+src)
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file.getvalue())
            await message.answer("Men buni saqlab qoydim,rahmat!")
    except Exception as e:
        await message.answer(e)

async def bot_echoall(message: types.document):
    print("Неправильная операция при отправке файла.")
    await message.answer("Rasm emas fayl yuborish kearak.")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(scan_doc,content_types=[types.ContentType.DOCUMENT],is_admin=True)
    dp.register_message_handler(bot_echoall,state="*", content_types=types.ContentTypes.ANY,is_admin=True)
