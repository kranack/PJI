import web
import mimetypes
import os

class public:
    def GET(self):
        public_dir = os.getcwd() + '/public'
        #public_dir = '/home/damien/Documents/S2/PJI/web/public'
        try:
            file_name = web.ctx.path.split('/')[-1]
            web.header('Content-type', mime_type(file_name))
            return open(public_dir + web.ctx.path, 'rb').read()
        except IOError:
            raise web.notfound()

def mime_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream' 
