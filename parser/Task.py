# coding=utf-8

#from path import path

import re
import os
import errno
import codecs

import Database

"""
Exemple de regex : (?P<priority>(\*+))(?P<string> [\w\s\dàé]+)(?P<date>\s*<[0-9]+/[0-9]+/[0-9]+>)?(?P<username>\s*@\w+)?(?P<tag>\s*:\w+:\s*)*(?P<ref>#\d+)?

"""

class Task: 

    def __init__(self):
    	self._db = Database.Database('database.db')
        self._title_pattern = '#\+([A-Z]+): ([/0-9a-zA-Z ]+)'
        #self._task_global = '(\*+)([ \w\dàé]+)(<[0-9]+/[0-9]+/[0-9]+>)?'
        self._task_keywords = ['DEADLINE', 'ASSIGN', 'FOLLOWERS', 'DEPENDS', 'SCHEDULED']
        self._task_status = ['DONE', 'NEXT']
        self._task_bloc = '(\*+)([\s\wàé:#<\/>@]+)'
        self._task_bloc_lines = '[^\n\r]+(?=\n|\z)'
        self._task_title = '(?<!@)([A-Z]+[éàa-z0-9 ]+)'
        self._task_date = '([A-Z]+)?:?\s+?([<0-9\/>]+)'
        self._task_user = '([A-Z]+)?:?\s+?(@\w+)'
        self._task_tag = ':(\w+):'
        self._task_ref = '#([0-9]+)'
        self._title_pattern = re.compile(self._title_pattern, re.UNICODE)
        #self._task_global = re.compile(self._task_global, re.UNICODE)
        self._task_bloc = re.compile(self._task_bloc, re.UNICODE)
        self._task_bloc_lines = re.compile(self._task_bloc_lines, re.UNICODE)
        self._task_title = re.compile(self._task_title, re.UNICODE)
        self._task_date = re.compile(self._task_date, re.UNICODE)
        self._task_user = re.compile(self._task_user, re.UNICODE)
        self._task_tag = re.compile(self._task_tag, re.UNICODE)
        self._task_ref = re.compile(self._task_ref, re.UNICODE)

    def parse(self, orgfile):
        #assert orgfile is FileType

        self._in = orgfile
        self._title_id = self.get_parse_text()
    
    def write(self, orgfile):
        self._out = orgfile
        self.write_parse_text()

    def get_parse_text(self):
    	flags = os.O_RDONLY
    	try:
            fd = os.open(self._in, flags)
        except OSError as err:
            if err.errno == errno.EEXIST:
                pass
            else:
                raise
        else:
		    with os.fdopen(fd, "rb") as fi:
		    	text = fi.read()
		    	fi.close()
        _titles = _tasks = _users = _tags = _refs = ""
        titles =  self._title_pattern.findall(text)

        if titles:
            for title in titles:
                #_titles += "#+{0}: {1}\n".format(title[0], title[1])
                _titles += "#+{0}: {1}\n".format(title[0], title[1])
        title_id = self._db.insert('Titles', [("raw_data", _titles)])
        
        # Tasks recursive search
        #
        # TODO: Record users, affialiations and refs
        #
        offset = 0
        task_id = 0
        next_id = 0
        bloc = self._task_bloc.search(text, offset)
        while bloc != None:
            #print tasks.groups()
            #print "({0},{1})\n".format(tasks.start(), tasks.end())
            print "Entrée dans le bloc : {0}".format(bloc.group(2))
            # Name search
            title_offset = 0
            title = self._task_title.search(bloc.group(2), title_offset)
            name = ""
            desc = ""
            status = 0
            while title != None:
                _status = re.sub('\s+', '', title.group(1))
            	if _status in self._task_status:
                    if _status == "DONE":
                        status = 1
                    elif _status == "NEXT":
                        status = 2
                elif name == "":
            		name = title.group(1)
            	title_offset = title.end()
            	title = self._task_title.search(bloc.group(2), title_offset)
           
            # Description Search
            lines = self._task_bloc_lines.findall(bloc.group(2))
            line_cpt = 0
            if lines:
                for line in lines:
                    if line_cpt > 0:
                        desc += "{0}\n".format(line)
                    line_cpt = line_cpt+1
            
            print "Name : {0}; Description: {1};".format(name, desc)
            # Date search
            
            dates = self._task_date.findall(bloc.group(2))
            deadline = scheduled = create = ""
            if dates:
            	for date in dates:
            		if date[0]:
            			if date[0] in self._task_keywords:
            				if date[0] == 'DEADLINE':
            					deadline = re.sub('<', '', date[1])
            				elif date[0] == 'SCHEDULED':
            					scheduled = re.sub('<', '', date[1])
            		else:
            			create = re.sub('<|>', '', date[1])
                        create = re.sub('/', '-', create)
            
            # Ref search

            refs = self._task_ref.findall(bloc.group(2))
            _ref = ""
            if refs:
                _ref = refs[0]
            
            # Record task
            if _ref != "":
	            next_id = int(_ref)
            else:
	        	next_id = task_id+1
            task_id = self._db.insert('Tasks', [("id", int(next_id)), ("name", name.decode('utf-8')), ("description", desc.decode('utf-8')), ("date_create", create), ("status", status), ("priority", bloc.group(1)), ("raw_titles", title_id)])
            
            # Tag search
            
            tags = self._task_tag.findall(bloc.group(2))
            if tags:
            	for tag in tags:
            		tag_id = self._db.insert('Tags', [("label", tag)])
            		self._db.insert('Attach_Tag', [("tag_id", tag_id), ("task_id", task_id)])

            # User search
            
            users = self._task_user.findall(bloc.group(2))
            if users:
            	for user in users:
            		if user[0]:
            			if user[0] in self._task_keywords:
            				if user[0] == 'ASSIGN':
		            			_users += "{0} affiliated to task #{1}\n".format(user[1], offset)
		            			#self._db.insert('Assign_Tasks', [])
		            		elif user[0] == 'FOLLOWERS':
		            			_users += "{0} follow task #{1}\n".format(user[1], offset)
		            			#self._db.insert('Follow_Tasks', [])
	            	else:
	            		_users += "{0} affiliated to task #{1}\n".format(user[1], offset)
            			#self._db.insert('Assign_Tasks', [])
            offset = bloc.end()
            
            # Display
            
            _tasks += "{0}{1}\n".format(bloc.group(1), bloc.group(2))
            
            # Search next task
            
            bloc = self._task_bloc.search(text, offset)
            
       	### End Bloc Search

        return title_id
    
    def to_db(self):
    	print "record to database"
    
    def from_db(self):
        res = ""
        titles = self._db.select('Titles', [("raw_data")], "id = {0}".format(self._title_id))
        tasks = self._db.select('Tasks', [("*")], "raw_titles = {0}".format(self._title_id))
        res += "{0}\n".format(titles[0][0])
        for task in tasks:
            res += "{0} ".format(task[6])
            if task[5] == 1:
                res += "DONE "
            elif task[5] == 2:
                res += "NEXT "
            res += u"{0}".format(task[1])
            if task[3] != "":
	            res += " <{0}>".format(task[3])
            res += " #{0}".format(task[0])
            if task[2] != "":
                res += "\n\n{0}".format(task[2])
            res += "\n\n"
            #res += task
        return res

    def write_parse_text(self):
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        
        if (os.path.exists(self._out)):
        	os.remove(self._out)
        
        try:
            fd = os.open(self._out, flags)
        except OSError as err:
            if err.errno == errno.EEXIST:
                pass
            else:
                raise
        else:
            with codecs.open(self._out, 'w', "utf-8") as fo:
            	fo.seek(0)
                text = self.from_db()
                fo.write(text)
                #fo.write(self._text)
                fo.truncate()
                fo.close()

