# coding=utf-8

import web
import json
import datetime

import Database
import parser.Parser
import parser.Task

class task:
  def GET(self):
    #recuperer le contenu d'un projet
    id_projet = web.ctx.path.split('/')[-1]
    projet = projet_from_db(id_projet)
    web.header('Content-Type', 'application/json')
    return json.dumps(projet)

class create:
  def POST(self):
    #mettre à jour le contenu d'un projet
    data = web.input()
    projet_to_db(data)
    response = dict()
    response["status"] = 1
    web.header('Content-Type', 'application/json')
    return json.dumps(response)

class delete:
  def POST(self):
    data = web.input()
    print data
    delete_task(data)
    response = dict()
    response["status"] = 1
    web.header('Content-Type', 'application/json')
    return json.dumps(response)

def projet_from_db(projet):
  db = Database.Database("../db/database.db")
  try:
    tasks = db.select("Tasks", ["*"], "raw_titles = {0}".format(projet))
    new_tasks = dict()
    for task in tasks:
      attach_tag = _db.select("Attach_Tag", ["tag_id"], "task_id={0}".format(task[0]))
      print attach_tag
      tags = list()
      for t in attach_tag:
          tag = _db.select("Tags", ["label"], "id={0}".format(t[0]))
          tags.append(tag)
      tagsTxt = ""
      for tag in tags:
          tagsTxt += ":{0}: ".format(tag[0][0])
      description = task[2]
      new = ""
      new_line = re.findall(r'(.*)\n', description)
      for n in new_line:
          new += re.sub(r'\n', '<br>', n)
      l = list(task)
      #l[2] = new
      l.append(tagsTxt)
      new_tasks[task[0]] = tuple(l)
    return new_tasks
  except Exception:
    raise web.notfound()

def projet_to_db(projet):
  db = Database.Database("db/database.db")
  try:
    last_id = db.select("Tasks", [("id")], "1 ORDER BY id DESC")[0][0]
    task = db.insert("Tasks", [("id", last_id+1), ("name", projet.task_name.decode('utf-8')), ("description", projet.task_description.decode('utf-8')), ("date_create", "{0}".format(datetime.datetime.now().date())),("raw_titles",  "{0}".format(projet.raw_titles))])
    return task
  except Exception:
    raise web.notfound()

def delete_task(task):
  db = Database.Database("db/database.db")
  db.delete("Tasks", "id = {0}".format(task.id))
