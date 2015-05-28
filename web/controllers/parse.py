# coding=utf-8

import web
import json

import Database
import parser.Parser
import parser.Task

class parse:
  def GET(self):
    #recuperer le contenu d'un projet
    id_projet = web.ctx.path.split('/')[-1]
    projet_from_db(id_projet)
    projet = web.header('Content-Type', 'application/json')
    return json.dumps(projet)
    
  def POST(self):
    #mettre à jour le contenu d'un projet
    return 0



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
