# coding=utf-8

#from path import path

import re
import os
import errno
import codecs

import Database
import Task

"""
Exemple de regex : (?P<priority>(\*+))(?P<string> [\w\s\dàé]+)(?P<date>\s*<[0-9]+/[0-9]+/[0-9]+>)?(?P<username>\s*@\w+)?(?P<tag>\s*:\w+:\s*)*(?P<ref>#\d+)?

"""

class Parser: 

    def __init__(self):
    	self._db = Database.Database('database.db')
        self._tasks = list()

        self._title_pattern = '#\+([A-Z]+): ([/0-9a-zA-Z ]+)'
        self._task_bloc = '(\*+)([\s\wàé:#<\/>@]+)'
        self._title_pattern = re.compile(self._title_pattern, re.UNICODE)
        self._task_bloc = re.compile(self._task_bloc, re.UNICODE)

    def parse(self, orgfile):
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
        bloc = self._task_bloc.search(text, offset)
        while bloc != None:
            #print tasks.groups()
            #print "({0},{1})\n".format(tasks.start(), tasks.end())
            print "Entrée dans le bloc : {0}".format(bloc.group(2))
            task = Task.Task()
            task_id = task.parse(bloc, title_id, task_id)
            self._tasks.append(task)
            

            offset = bloc.end()
            
            # Display
            
            _tasks += "{0}{1}\n".format(bloc.group(1), bloc.group(2))
            
            # Search next task
            
            bloc = self._task_bloc.search(text, offset)
            
       	### End Bloc Search

        return title_id
    
    
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
                #text = self.from_db()
                txtToPrint = ""
                txtToPrint += self._tasks[0].titles_from_db()
                for task in self._tasks:
                    txtToPrint += task.from_db()
                fo.write(txtToPrint)
                #fo.write(self._text)
                fo.truncate()
                fo.close()

