# coding=utf-8

#from path import path

import re
import os
import errno

import Database

"""
Exemple de regex : (?P<priority>(\*+))(?P<string> [\w\s\dàé]+)(?P<date>\s*<[0-9]+/[0-9]+/[0-9]+>)?(?P<username>\s*@\w+)?(?P<tag>\s*:\w+:\s*)*(?P<ref>#\d+)?

"""

class Parser: 

    def __init__(self):
    	self._db = Database.Database('database.db')
        self._title_pattern = '#\+([A-Z]+): ([/0-9a-zA-Z ]+)'
        #self._task_global = '(\*+)([ \w\dàé]+)(<[0-9]+/[0-9]+/[0-9]+>)?'
        self._task_keywords = ['DEADLINE', 'ASSIGN', 'FOLLOWERS', 'DEPENDS', 'SCHEDULED']
        self._task_bloc = '(\*+)([\s\wàé:#<\/>@]+)'
        self._task_title = '([A-Z]+[a-z0-9 ]+)'
        self._task_date = '([A-Z]+)?:?\s+?([<0-9\/>]+)'
        self._task_user = '([A-Z]+)?:?\s+?(@\w+)'
        self._task_tag = '(:\w+:)'
        self._task_ref = '(#[0-9]+)'
        self._title_pattern = re.compile(self._title_pattern, re.UNICODE)
        #self._task_global = re.compile(self._task_global, re.UNICODE)
        self._task_bloc = re.compile(self._task_bloc, re.UNICODE)
        self._task_title = re.compile(self._task_title, re.UNICODE)
        self._task_date = re.compile(self._task_date, re.UNICODE)
        self._task_user = re.compile(self._task_user, re.UNICODE)
        self._task_tag = re.compile(self._task_tag, re.UNICODE)
        self._task_ref = re.compile(self._task_ref, re.UNICODE)

    def start(self, orgfile):
        #assert orgfile is FileType

        self._in = orgfile
        self._text = self.get_parse_text()
    
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
                 _titles += "{0} => {1}\n".format(title[0], title[1])
        
        # Tasks recursive search
        #
        # TODO: Save all matches in a list. 
        #       Search users, tags and refs between two matches.
        #       Record tasks, users, tags and refs
        #
        offset = 0
        bloc = self._task_bloc.search(text, offset)
        while bloc != None:
            #print tasks.groups()
            #print "({0},{1})\n".format(tasks.start(), tasks.end())
            
            # Name search
            

            # Date search
            
            dates = self._task_date.findall(bloc.group(2))
            deadline = scheduled = create = ""
            if dates:
            	for date in dates:
            		if date[0]:
            			if date[0] in self._task_keywords:
            				if date[0] == 'DEADLINE':
            					deadline = date[1]
            				elif date[0] == 'SCHEDULED':
            					scheduled = date[1]
            		else:
            			create = date[1]
            
            # Record task
            
            task_id = self._db.insert('Tasks', [("name", name), ("date_create", create)])
            
            # Tag search
            
            tags = self._task_tag.findall(bloc.group(2))
            if tags:
            	for date in dates:
            		# Record tags
            
            # User search
            
            users = self._task_user.findall(bloc.group(2))
            if users:
            	for user in users:
            		if user[0]:
            			if user[0] in self._task_keywords:
            				if user[0] == 'ASSIGN':
		            			_users += "{0} affiliated to task #{1}\n".format(user[1], offset)
		            		elif user[0] == 'FOLLOWERS':
		            			_users += "{0} follow task #{1}\n".format(user[1], offset)
	            	else:
	            		_users += "{0} affiliated to task #{1}\n".format(user[1], offset)
            offset = bloc.end()
            
            # Display
            
            _tasks += "{0} => {1}\n".format(bloc.group(1), bloc.group(2))
            
            # Search next task
            
            bloc = self._task_bloc.search(text, offset)
        
        #tasks = self._task_global.findall(text)
        #if tasks:
        #    for task in tasks:
        #        _tasks += "{0} => {1} {2}\n".format(task[0], task[1], task[2])
        #users = self._task_user.findall(text)
        #if users:
        #    for user in users:
        #        if user != '':
        #            _users += "'{0}'\n".format(user)
        #tags = self._task_tag.findall(text)
        #if tags:
        #    for tag in tags:
        #        if tag != '':
        #            _tags += "{0}\n".format(tag)
        #refs = self._task_ref.findall(text)
        #if refs:
        #    for ref in refs:
        #        if ref != '':
        #            _refs += "{0}\n".format(ref)

        return "Infos:\n\n{0}\nTasks:\n\n{1}\nUsers:\n\n{2}".format(_titles, _tasks, _users)

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
            with os.fdopen(fd, 'w') as fo:
            	fo.seek(0)
                fo.write(self._text)
                fo.truncate()
                fo.close()

