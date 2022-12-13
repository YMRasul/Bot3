import sqlite3 as sq

def sql_start():
    global base,cur
    base = sq.connect('client.db')
    cur = base.cursor()
    if base:
        print('подключение к базе данных OK!')
    base.execute('''CREATE TABLE IF NOT EXISTS client (idp INTEGER PRIMARY KEY NOT NULL, phone INTEGER, innorg INTEGER,fio TEXT,prz INTEGER)''')
    base.commit()

async def users_add(state):
    async with state.proxy() as data:
        t = tuple(data.values())

    print(t)

    r = cur.execute('SELECT idp FROM client WHERE idp == ?',(t[0],)).fetchone()

    if r==None:
        cur.execute('INSERT INTO client VALUES (?,?,?,?,?)',(t[0],t[1],t[3],t[2],0))
    else:
        #print(r,t)
        cur.execute('UPDATE client SET  phone==?,innorg==?,fio==? WHERE idp ==?' , (t[1],t[3],t[2],r[0]))

    base.commit()


async def inn_client(idx):
        r = cur.execute('SELECT innorg,phone,fio FROM client WHERE idp == ?',(idx,)).fetchone()
        return(r)