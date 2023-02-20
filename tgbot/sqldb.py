import sqlite3 as sq
from sqlite3 import Error


class Database:
    def __init__(self, dbFile):
        self.base = sq.connect(dbFile)
        self.cur = self.base.cursor()
        tables = '''CREATE TABLE IF NOT EXISTS client (idp INTEGER PRIMARY KEY NOT NULL, phone INTEGER,innorg INTEGER,fio TEXT,prz INTEGER);
        CREATE TABLE IF NOT EXISTS org (inn INTEGER PRIMARY KEY NOT NULL, prz INTEGER, nam TEXT);
        PRAGMA foreign_keys=on;
        CREATE TABLE  IF NOT EXISTS admin ( admin_id INTEGER NOT NULL, org INTEGER NOT NULL, fio TEXT, PRIMARY KEY ( admin_id, org ),FOREIGN KEY (org ) REFERENCES org (inn) ON DELETE CASCADE);'''
        #print("tables=",tables)
        self.cur.executescript(tables)

    async def fkeys(self):
        r = self.cur.execute('PRAGMA foreign_keys').fetchall()
        return r

    def message(self, mess):
        print(mess)

    def close(self):
        self.cur.close()
        self.base.close()


    async def user_exists(self, state):
        async with state.proxy() as data:
            t = tuple(data.values())
        with self.base:
            r = self.cur.execute('SELECT idp FROM client WHERE idp == ?', (t[0],)).fetchmany(1)
            return bool(len(r))

    async def user_exists2(self, id):
        with self.base:
            return self.cur.execute('SELECT idp,fio,phone,innorg FROM client WHERE idp == ?', (id,)).fetchone()
    async def add_user(self, state, time):
        async with state.proxy() as data:
            t = tuple(data.values())
        #print(time, "Insert", t)
        with self.base:
            return self.cur.execute('INSERT INTO client VALUES (?,?,?,?,?)', (t[0], t[1], t[3], t[2], 1,))

    async def up_user(self, state, time):
        async with state.proxy() as data:
            t = tuple(data.values())
        #print(time, "Update", t)
        with self.base:
            self.cur.execute('UPDATE client SET  phone==?,innorg==?,fio==? WHERE idp ==?', (t[1], t[3], t[2], t[0],))

    async def get_inn(self, idx):
        with self.base:
            r = self.cur.execute('SELECT innorg,phone,fio,prz,\
             (select nam from org where (client.innorg=org.inn) ) FROM client WHERE idp == ?', (idx,)).fetchone()
        return (r)

    async def innUser(self,inn,prz):
        with self.base:
            r = self.cur.execute('select count(*) from client where (innorg==? and prz==?)',(inn,prz,)).fetchone()
            return (r)
    async def get_rek(self, idx):
        with self.base:
            r = self.cur.execute('SELECT org,fio FROM admin WHERE admin_id == ?', (idx,)).fetchall()
            #print(r)
        return (r)

    async def get_users(self):
        with self.base:
            return self.cur.execute('SELECT idp,fio,prz,innorg  FROM   client').fetchall()
    async def get_users_org(self,inn):
        #print(inn)
        with self.base:
            r = self.cur.execute('SELECT idp,fio,prz FROM client WHERE innorg==?' ,(inn,)).fetchall()
            return r

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
        r = self.cur.execute('SELECT admin_id FROM admin WHERE (admin_id == ? and org== ?)', (id,innorg,)).fetchone()
        #print(r)
        if r==None:
            with self.base:
                self.cur.execute('INSERT INTO admin VALUES (?,?,?)', (id,innorg,fio,))
                #print('Insert')
        else:
            with self.base:
                self.cur.execute('UPDATE admin SET fio==? WHERE (admin_id ==? and org==?)', (fio,id,innorg,))
                #print('Update')
        return r
    async def admin_del(self, id,inn):
        with self.base:
            return self.cur.execute('DELETE FROM admin WHERE (admin_id==? and org==?)', (id,inn,))
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
            from admin order by admin_id,org').fetchall()
    async def inn_info(self):
        with self.base:
            return self.cur.execute('select inn,prz,nam from org order by inn').fetchall()
    async def inn_rek(self,inn):
        with self.base:
            return self.cur.execute('select nam from org WHERE inn == ?', (inn,)).fetchone()

    def createTable(self, table):
        with self.base:
            print(table)
            self.cur.execute(table)
    async def droporg(self):
        with self.base:
            self.cur.execute('DROP TABLE org')
            s = '''CREATE TABLE IF NOT EXISTS org (inn INTEGER PRIMARY KEY NOT NULL, prz INTEGER, nam TEXT)'''
            self.createTable(s)
    async def dropadm(self):
        with self.base:
            s = 'DROP TABLE admin'

            print(s)
            self.cur.execute(s)

            s = 'PRAGMA foreign_keys=on'
            print(s)
            self.cur.execute(s)
            s = '''CREATE TABLE admin ( admin_id INTEGER NOT NULL, org INTEGER NOT NULL, fio TEXT, PRIMARY KEY ( admin_id, org ),\
			 FOREIGN KEY (org ) REFERENCES org (inn) ON DELETE CASCADE)'''
            #s ='''CREATE TABLE IF NOT EXISTS admin (admin_id INTEGER NOT NULL,org INTEGER NOT NULL,fio TEXT, PRIMARY KEY (admin_id, org ) )'''
            print(s)
            self.createTable(s)

    async def inn_add(self, inn, prz,nam):
        with self.base:
            r = self.cur.execute('SELECT inn FROM org WHERE inn == ?', (inn,)).fetchmany(1)
            if bool(len(r)):
                self.cur.execute('UPDATE org SET  prz==?, nam==? WHERE inn==?', (prz,nam,inn,))
                #print("Update", inn,prz,nam)
            else:
                self.cur.execute('INSERT INTO org VALUES (?,?,?)', (inn, prz,nam,))
                #print("Insert",inn,prz,nam)
    async def inn_del(self, inn):
        with self.base:
            #self.cur.execute('DELETE FROM admin WHERE org==?', (inn,))

            # из таблицы admin записи удальяются каскадно
            self.cur.execute('DELETE FROM org WHERE inn==?', (inn,))
        #print("Delete cascade", inn)
    async def reg_id(self, id, inn, tel, fio):
        with self.base:
            r = self.cur.execute('SELECT idp FROM client WHERE idp == ?', (id,)).fetchone()
            #print(r)
            if (r):
                #print('Update')
                self.cur.execute('UPDATE client SET  phone==?,innorg==?,fio==? WHERE idp ==?', (tel, inn,fio, id,))
            else:
                #print('Insert')
                return self.cur.execute('INSERT INTO client VALUES (?,?,?,?,?)', (id, tel, inn, fio, 0,))

    async def clients(self):
        with self.base:
            return self.cur.execute('select prz,innorg,idp,phone,fio from client order by innorg,idp').fetchall()


    async def get_innfio(self, id,inn):
        with self.base:
            return (self.cur.execute('SELECT fio from admin  WHERE (admin_id == ? and org==?)', (id,inn,)).fetchone())
    async def get_innorg(self, id):
        with self.base:
            return (self.cur.execute('SELECT org from admin  WHERE admin_id == ?', (id,)).fetchall())

    async def poisk_id(self, user_id):
        inns = []
        r = await self.get_innorg(user_id)
        n = len(r)
        if n > 0:
            for i in range(n):
                inns.append(r[i][0])
        return inns

async def create_connection(dbFile):
    ''' Это отделная функция для подключение к базе данных'''
    connection = None
    try:
        connection = sq.connect(dbFile)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection
