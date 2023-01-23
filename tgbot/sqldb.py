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
            '''CREATE TABLE IF NOT EXISTS org (inn INTEGER PRIMARY KEY NOT NULL, prz INTEGER, nam TEXT)''',
            '''CREATE TABLE IF NOT EXISTS admin  (admin_id INTEGER PRIMARY KEY NOT NULL,org INTEGER,fio Text)'''
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
    async def get_rek(self, idx):
        with self.base:
            r = self.cur.execute('SELECT org,fio,(select nam FROM org WHERE (admin.org=org.inn)) \
            FROM admin WHERE admin_id == ?', (idx,)).fetchone()
        return (r)

    async def get_users(self):
        with self.base:
            return self.cur.execute('SELECT idp,fio,prz,innorg  FROM   client').fetchall()
    async def get_users_org(self,inn):
        with self.base:
            return self.cur.execute('SELECT idp,fio,prz  FROM client WHERE innorg==?',(inn,)).fetchall()

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
    async def admin_add(self, id,innorg,fio):
        r = self.cur.execute('SELECT admin_id FROM admin WHERE admin_id == ?', (id,)).fetchone()
        if r==None:
            with self.base:
                self.cur.execute('INSERT INTO admin VALUES (?,?,?)', (id,innorg,fio,))
        else:
            with self.base:
                self.cur.execute('UPDATE admin SET org==?,fio==? WHERE admin_id ==?', (innorg,fio,id,))
        return r
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
            return self.cur.execute('select admin_id,fio,org,(select nam FROM org WHERE (admin.org=org.inn))\
            from admin').fetchall()
    async def inn_info(self):
        with self.base:
            return self.cur.execute('select inn,prz,nam from org').fetchall()
    async def inn_rek(self,inn):
        with self.base:
            return self.cur.execute('select nam from org WHERE inn == ?', (inn,)).fetchone()
    async def droporg(self):
        with self.base:
            self.cur.execute('DROP TABLE org')
            s = '''CREATE TABLE IF NOT EXISTS org (inn INTEGER PRIMARY KEY NOT NULL, prz INTEGER, nam TEXT)'''
            self.createTable(s)
    async def dropadm(self):
        with self.base:
            self.cur.execute('DROP TABLE admin')
            s ='''CREATE TABLE IF NOT EXISTS admin  (admin_id INTEGER PRIMARY KEY NOT NULL,org INTEGER,fio Text)'''
            self.createTable(s)

    async def inn_add(self, inn, prz,nam):
        with self.base:
            r = self.cur.execute('SELECT inn FROM org WHERE inn == ?', (inn,)).fetchmany(1)
            if bool(len(r)):
                if prz == 9:
                    #print("Delete ",inn)
                    self.cur.execute('DELETE FROM org WHERE inn==?', (inn,))
                else:
                    self.cur.execute('UPDATE org SET  prz==?, nam==? WHERE inn==?', (prz,nam,inn,))
                    #print("Update", inn,prz,nam)
            else:
                self.cur.execute('INSERT INTO org VALUES (?,?,?)', (inn, prz,nam,))
                #print("Insert",inn,prz,nam)

    async def reg_id(self, user_id, inn, tel):
        with self.base:
            r = self.cur.execute('SELECT idp FROM client WHERE idp == ?', (user_id,)).fetchmany(1)
            #print(r)
            if bool(len(r)):
                #print('Update')
                self.cur.execute('UPDATE client SET  phone==?,innorg==?,prz==? WHERE idp ==?', (tel, inn, 1, user_id,))
            else:
                #print('Insert')
                return self.cur.execute('INSERT INTO client VALUES (?,?,?,?,?)', (user_id, tel, inn, '', 1,))

    async def get_innorg(self, id):
        with self.base:
            return (self.cur.execute('SELECT org,fio from admin  WHERE admin_id == ?', (id,)).fetchone())

    async def poisk_id(self, user_id, fileName):
        e = True
        r = await self.get_innorg(user_id)
        if r:
            innClient = r[0]
            try:
                innFile = int(fileName[0:9])
                e = (innFile == innClient)
                ''' 
                if e:
                    print(fileName, user_id, "Может сохранить...", "innFile", innFile, "==", innClient, "innVadmin")
                else:
                    print(fileName, user_id, "Не может сохранить...", "innFile", innFile, "!=", innClient, "innVadmin")
                '''
            except:
                #print(fileName, "Не может быт сохранен..")
                e = False
        else:
            e = False
            #print(user_id, "нет в таблице ADMIN")
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
