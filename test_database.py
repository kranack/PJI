import Database

test = Database.Database('database.db')

res = test.select('Tasks')

print res
