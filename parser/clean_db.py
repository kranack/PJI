import Database

db = Database.Database('database.db')

db.delete('Assign_Tasks', '1')
db.delete('Depend_Tasks', '1')
db.delete('Follow_Tasks', '1')
db.delete('Attach_Tag', '1')
db.delete('Tasks', '1')
db.delete('Tags', '1')
db.delete('Users', '1')
