# coding=utf-8

from path import path

import re
import os
import errno

class Parser: 

    def __init__(self):
        self._title_pattern = '#\+([A-Z]+): ([/0-9a-zA-Z ]+)'
        self._task_pattern = '(\*+)([\w\s\dàé]+)(@\w+\s+)?(<[0-9]+/[0-9]+/[0-9]+>)?(:\w+:\s+)*(#[0-9]+)*'
        self._title_pattern = re.compile(self._title_pattern, re.UNICODE)
        self._task_pattern = re.compile(self._task_pattern, re.UNICODE)

    def start(self, orgfile):
        #assert orgfile is FileType

        self._in = orgfile
        self._text = self.get_parse_text()
    
    def write(self, orgfile):
        self._out = orgfile
        self.write_parse_text

    def get_parse_text(self):
        text = path(self._in).bytes()
        _titles = _tasks = ""        
        titles =  self._title_pattern.findall(text)

        if titles:
            for title in titles:
                 _titles += "{0} => {1}\n".format(title[0], title[1])

        tasks = self._task_pattern.findall(text)
        if tasks:
            for task in tasks:
                _tasks += "{0} => {1} {2} {3}\n".format(task[0], task[1], task[2], task[3])

        return _titles + _tasks

    def write_parse_text(self):
        print "begin to write"
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        
        try:
            fd = os.open(self._out, flags)
        except OSError as err:
            if err.errno == errno.EEXIST:
                pass
            else:
                raise
        else:
            with os.fdopen(fd, 'w') as fo:
                fo.write(self._text)
                fo.close()

        print "write ok"
