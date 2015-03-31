import sqlite3
import string

class Database(object):

    def __init__(self, database):
        self._db = database
        self._conn = sqlite3.connect(database)
        self._curs = self._conn.cursor()
        self.list_tables()
    
    def __exit__(self):
        self._conn.commit()
        self._conn.close()

    def list_tables(self):
        self._curs.execute('select name from sqlite_master where type=\'table\'')
        self._tab = []
        for table in self._curs:
            self._tab.append(table[0])
    
    def format_string(self, string, table, args=[]):
        if table in self._tab:
            if not args:
                string = str.replace(string, ":tab", table)
            else:
                cols = "%s ( %s )" % (table, ",".join(args))
                string = str.replace(string, ":tab", cols)
            return string
        else:
            raise Exception("%s does not exists in %s" % (table, self._db))

    def select(self, table, fields=[], cond=1):
        f= ""
        if not fields:
            f = "*"
        else:
            for field in fields:
                f += field+", "
            f = f[:-1]
        sql = "SELECT :fields FROM :tab WHERE ?"
        sql = self.format_string(sql, table)
        sql = str.replace(sql, ":fields", f)
        
        self._curs.execute(sql, [cond])
        return self._curs.fetchall()

    def insert(self, table, values):
        sql = "INSERT INTO :tab VALUES (?)"
        val = ""
        cols = []
        for Key,Value in values:
            cols.append(Key)
            val += "'%s'," % Value
        val = val[:-1]
        sql = self.format_string(sql, table, cols)
        sql = str.replace(sql, "?", val)
        
        self._curs.execute(sql)
        self._conn.commit()
        return self._curs.lastrowid

    def update(self, table, values, cond=1):
        sql = "UPDATE :tab SET :val WHERE ?"
        val = ""
        for Key,Value in values:
            val += "{0}='{1}',".format(Key, Value)
        val = val[:-1]
        sql = self.format_string(sql, table)
        sql = str.replace(sql, ":val", val)
        sql = str.replace(sql, "?", cond)
        
        print sql
        self._curs.execute(sql)
        self._conn.commit()

    def delete(self, table, cond=1):
        sql = "DELETE FROM :tab WHERE ?"
        sql = self.format_string(sql, table)
        sql = str.replace(sql, "?", cond)
		# Reset auto-increment
        internal_sql = "DELETE FROM SQLITE_SEQUENCE WHERE name= '?'"
        internal_sql = str.replace(internal_sql, "?", table)
		
        print sql
        self._curs.execute(sql)
        self._curs.execute(internal_sql)
        self._curs.execute("VACUUM")
        self._conn.commit()
        
