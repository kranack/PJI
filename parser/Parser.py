# coding=utf-8

from path import path

import re
import os
import errno

"""
Exemple de regex : (?P<priority>(\*+))(?P<string> [\w\s\dàé]+)(?P<date>\s*<[0-9]+/[0-9]+/[0-9]+>)?(?P<username>\s*@\w+)?(?P<tag>\s*:\w+:\s*)*(?P<ref>#\d+)?

"""

class Parser: 

    def __init__(self):
        self._title_pattern = '#\+([A-Z]+): ([/0-9a-zA-Z ]+)'
        self._task_global = '(\*+)([\w\s\dàé]+)(<[0-9]+/[0-9]+/[0-9]+>)?'
        self._task_user = '(@\w+)?'
        self._task_tag = '(:\w+\s+:)*'
        self._task_ref = '(#[0-9]+)*'
        self._title_pattern = re.compile(self._title_pattern, re.UNICODE)
        self._task_global = re.compile(self._task_global, re.UNICODE)
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
        text = path(self._in).bytes()
        _titles = _tasks = _users = _tags = _refs = ""
        titles =  self._title_pattern.findall(text)

        if titles:
            for title in titles:
                 _titles += "{0} => {1}\n".format(title[0], title[1])

        tasks = self._task_global.findall(text)
        if tasks:
            for task in tasks:
                _tasks += "{0} => {1} {2}\n".format(task[0], task[1], task[2])
        users = self._task_user.findall(text)
        if users:
            for user in users:
                if user != '':
                    _users += "'{0}'\n".format(user)
        tags = self._task_tag.findall(text)
        if tags:
            for tag in tags:
                if tag != '':
                    _tags += "{0}\n".format(tag)
        refs = self._task_ref.findall(text)
        if refs:
            for ref in refs:
                if ref != '':
                    _refs += "{0}\n".format(ref)
        print _refs
        print _tags
        print _users
        print _tasks
        return _titles + _tasks

    def write_parse_text(self):
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

