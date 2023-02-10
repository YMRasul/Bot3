from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
def gen_markup(texts: list, prefix: str, row_width: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=row_width,one_time_keyboard=True)
    for num, text in enumerate(texts):
        if num<12:
            markup.insert(InlineKeyboardButton(f"{text}", callback_data=f"{text}"))
        else:
            markup.insert(InlineKeyboardButton(f"{text}", callback_data=f"{prefix}"))
    return markup

