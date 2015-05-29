# coding=utf-8
import os
import errno
import codecs

import Database
import parser.Task

class parse:
  def __init__(self):
    self._db = Database.Database("db/database.db")

  def project_from_task(self, task_id):
    project = self._db.select("Tasks", ["raw_titles"], "id = {0}".format(task_id))
    self._id = project[0][0]
    return self._id

  def export_project(self, project_id):
    tasks = self._db.select("Tasks", ["*"], "raw_titles = {0}".format(project_id))
    print tasks
    self._tasks = list()
    for task in tasks:
      t = parser.Task.Task()
      t.associate(task[0], project_id)
      self._tasks.append(t)
    
    ret = ""
    for ta in self._tasks:
      ret += ta.from_db()

    if (os.path.exists('output/Test.org')):
      os.remove('output/Test.org')

    try:
      fd = os.open('output/Test.org', os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except OSError as err:
      if err.errno == errno.EEXIST:
        pass
      else:
        raise
    else:
      with codecs.open('output/Test.org', 'w', 'utf-8') as fo:
        fo.seek(0)
        fo.write(ret)
        fo.truncate()
        fo.close()
