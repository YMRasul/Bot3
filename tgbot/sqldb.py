import sqlite3 as sq
from sqlite3 import Error


class Database:
    def __init__(self, dbFile):
        self.base = sq.connect(dbFile)
        self.cur = self.base.cursor()
        self.createTables()

    def createTables(self):
        tables = [
            '''CREATE TABLE IF NOT EXISTS client (idp INTEGER PRIMARY KEY NOT NULL, phone INTEGER,innorg INTEGER,fio TEXT,prz INTEGER)''',
            '''CREATE TABLE IF NOT EXISTS org (inn INTEGER PRIMARY KEY NOT NULL, prz INTEGER)''',
            '''CREATE TABLE IF NOT EXISTS admin  (admin_id INTEGER PRIMARY KEY NOT NULL)'''
        ]
        for tab in tables:
#            print(tab)
            self.createTable(tab)

    def message(self, mess):
        print(mess)

    def close(self):
        self.cur.close()
        self.base.close()

    def createTable(self, table):
        with self.base:
            self.cur.execute(table)

    async def user_exists(self, state):
        async with state.proxy() as data:
            t = tuple(data.values())
        with self.base:
            r = self.cur.execute('SELECT idp FROM client WHERE idp == ?', (t[0],)).fetchmany(1)
            return bool(len(r))

    async def add_user(self, state, time):
        async with state.proxy() as data:
            t = tuple(data.values())
        print(time, "Insert", t)
        with self.base:
            return self.cur.execute('INSERT INTO client VALUES (?,?,?,?,?)', (t[0], t[1], t[3], t[2], 1,))

    async def up_user(self, state, time):
        async with state.proxy() as data:
            t = tuple(data.values())
        print(time, "Update", t)
        with self.base:
            self.cur.execute('UPDATE client SET  phone==?,innorg==?,fio==? WHERE idp ==?', (t[1], t[3], t[2], t[0],))

    async def get_inn(self, idx):
        with self.base:
            r = self.cur.execute('SELECT innorg,phone,fio,prz FROM client WHERE idp == ?', (idx,)).fetchone()
        return (r)

    async def get_users(self):
        with self.base:
            return self.cur.execute('SELECT idp,fio,prz,innorg  FROM   client').fetchall()

    async def set_active(self, prz, user_id):
        with self.base:
            return self.cur.execute('UPDATE client SET  prz==? WHERE idp==?', (prz, user_id,))

    async def inn_exists(self, state):
        async with state.proxy() as data:
            t = tuple(data.values())
        with self.base:
            r = self.cur.execute('SELECT inn FROM org WHERE inn == ?', (t[3],)).fetchmany(1)  # t[3] = inn
            return bool(len(r))

    async def inn_exists2(self, user_inn):
        with self.base:
            r = self.cur.execute('SELECT inn FROM org WHERE inn == ?', (user_inn,)).fetchmany(1)
            return bool(len(r))
    async def admin_exists(self, id):
        with self.base:
            r = self.cur.execute('SELECT admin_id FROM admin WHERE admin_id == ?', (id,)).fetchmany(1)
            return bool(len(r))
    async def admin_add(self, id):
        with self.base:
            return self.cur.execute('INSERT INTO admin VALUES (?)', (id,))
    async def admin_del(self, id):
        with self.base:
            return self.cur.execute('DELETE FROM admin WHERE admin_id==?', (id,))
    async def admins(self):
        x = []
        with self.base:
            r = self.cur.execute('SELECT admin_id FROM  admin').fetchall()
        if len(r)!=0:
           for i in r:
               x.append(i[0])
        return x

    async def admins_info(self):
        with self.base:
            return self.cur.execute('select admin_id,\
                                            (select client.innorg from client where client.idp=admin.admin_id),\
                                            (select client.phone from client where client.idp=admin.admin_id),\
                                            (select client.fio from client where client.idp=admin.admin_id) \
                                     from admin').fetchall()

    async def inn_add(self, inn, prz):
        with self.base:
            r = self.cur.execute('SELECT inn FROM org WHERE inn == ?', (inn,)).fetchmany(1)
            if bool(len(r)):
                if prz == 9:
                    print("Delete INN " + str(inn))
                    self.cur.execute('DELETE FROM org WHERE inn==?', (inn,))
                else:
                    print("Update INN ")
                    self.cur.execute('UPDATE org SET  prz==? WHERE inn==?', (prz, inn,))
            else:
                print("Insert INN ")
                self.cur.execute('INSERT INTO org VALUES (?,?)', (inn, prz,))

    async def reg_id(self, user_id, inn, tel):
        with self.base:
            r = self.cur.execute('SELECT idp FROM client WHERE idp == ?', (user_id,)).fetchmany(1)
            print(r)
            if bool(len(r)):
                print('Update')
                self.cur.execute('UPDATE client SET  phone==?,innorg==?,prz==? WHERE idp ==?', (tel, inn, 1, user_id,))
            else:
                print('Insert')
                return self.cur.execute('INSERT INTO client VALUES (?,?,?,?,?)', (user_id, tel, inn, '', 1,))

    async def poisk_id(self, user_id, fileName):
        e = True
        try:
            innFile = int(fileName[0:9])
            r = await self.get_inn(user_id)
            innClient = r[0]

            x = await self.inn_exists2(innClient)

            if x:
                e = (innFile == innClient)

                if e:
                    print(fileName, user_id, "Может сохранить...", "innFile", innFile, "==", innClient, "innClient")
                else:
                    print(fileName, user_id, "Не может сохранить...", "innFile", innFile, "!=", innClient, "innClient")
            else:
                print(innClient, "нет в таблице ORG")
                e = False
        except:
            e = False
            print(fileName, 'Не может быть сохранен ...', user_id)

        return e


async def create_connection(dbFile):
    ''' Это отделная функция для подключение к базе данных'''
    connection = None
    try:
        connection = sq.connect(dbFile)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection
