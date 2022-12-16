from .sqldb import Database


async def createTables(db):
    tables = [
        '''CREATE TABLE IF NOT EXISTS client (user_id INTEGER PRIMARY KEY NOT NULL, phone INTEGER,fio TEXT,active INTEGER)''',
        '''CREATE TABLE IF NOT EXISTS org (id INTEGER PRIMARY KEY NOT NULL, nam)'''
    ]
    try:
        e = 1
        baza = Database(db)
        print('Подключение к базе данных ...')
        # Создание таблиц
        for tab in tables:
            await baza.createTable(tab)
    except:
        e=0
        print('Нет связи с базой данных ...')

    return e

