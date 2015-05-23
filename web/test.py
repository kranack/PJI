import re
import web
import mimetypes
import db.Database

t_globals = dict(
  datestr=web.datestr,
)

render = web.template.render('templates/', globals=t_globals)
render._keywords['globals']['render'] = render

urls = (
        '/', 'index',
        '/(?:img|js|css)/.*', 'public',
        )

def mime_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

# Images, Javascript and css files
class public:
    def GET(self):
        public_dir = 'public'
        try:
            file_name = web.ctx.path.split('/')[-1]
            web.header('Content-type', mime_type(file_name))
            return open(public_dir + web.ctx.path, 'rb').read()
        except IOError:
            raise web.notfound()

# Index class for homepage
class index:
    def GET(self):
    	_db = db.Database.Database("db/database.db")
        tasks = _db.select("Tasks")
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
        return render.index(new_tasks)



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
