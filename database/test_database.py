import Database

test = Database.Database('database.db')

res = test.select('Tasks')
for row in res:
    print '#{0}: {1} ajoutee le {2}'.format(row[0], row[1], row[2])

#test.insert('Tasks', [("name", "Test"), ("date_create", "2015-02-17")])
test.update('Tasks', [("name", "Test1")], "id='1'")
