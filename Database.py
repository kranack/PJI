import sqlite3

class Database(object):

    def __init__(self, database):
        self._db = database
        self._conn = sqlite3.connect(database)
        self._curs = self._conn.cursor()
    
    def __exit__(self):
        self._conn.commit()
        self._conn.close()

    def select(self, table, fields=[], cond=1):
        f= ""
        if not fields:
            f = "*"
        else:
            for field in fields:
                f += field+", "
            f = f[:-1]
        #self._curs.execute("SELECT ? FROM ? WHERE ?", [f, table, cond])
        self._curs.execute("SELECT :fields FROM :from WHERE :cond", {"fields": f, "from": table, "cond": cond})
        
        return self._curs.fetchall()
