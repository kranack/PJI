import re
import web
import mimetypes
import controllers.Database
import controllers.public
import controllers.task

t_globals = dict(
  datestr=web.datestr,
)

render = web.template.render('templates/', globals=t_globals)
render._keywords['globals']['render'] = render

urls = (
        '/', 'index',
        '/task', controllers.task.task,
        '/task/create', controllers.task.create,
        '/task/delete', controllers.task.delete,
        '/(?:img|js|css|fonts)/.*', controllers.public.public,
        )


# Index class for homepage
class index:
    def GET(self):
    	_db = controllers.Database.Database("db/database.db")
        tasks = _db.select("Tasks")
        raw_title = _db.select("Titles", [("id")])
        new_tasks = list()
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
            new_tasks.append(tuple(l))
        return render.index(raw_title[0][0], new_tasks)



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
