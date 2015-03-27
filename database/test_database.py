import Database

test = Database.Database('database.db')

test.insert('Tasks', [("name", "Test1"), ("date_create", "2015-02-17")])

before = test.select('Tasks')
for row in before:
    print '#{0}: {1} ajoutee le {2}'.format(row[0], row[1], row[2])

#test.insert('Tasks', [("name", "Test"), ("date_create", "2015-02-17")])
#test.update('Tasks', [("name", "Test1")], "id='1'")
test.delete('Tasks', "1")

after = test.select('Tasks')
for row in after:
    print '#{0}: {1} ajoutee le {2}'.format(row[0], row[1], row[2])
