from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from create_bot import today

y = int(today.strftime("%Y"))
m = int(today.strftime("%m"))

#print('------------------------------------------------------------',today)

i = 12
mas = []

while (i > 0):
    m = m - 1
    if m == 0:
        m = 12
        y = y - 1
    s = str(y) + '_' + str(m).rjust(2, '0')
    mas.append(s)
    i = i - 1

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)  # 1 - настраивается по экрану
# 2 - спрятат после нажатие
b = []
for i in range(12):
    b.append(KeyboardButton(mas[i]))

kb_client.row(b[0], b[1], b[2], b[3])
kb_client.row(b[4], b[5], b[6], b[7])
kb_client.row(b[8], b[9], b[10], b[11])

