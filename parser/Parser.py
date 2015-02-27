# coding=utf-8

from path import path

import re

class Parser: 

    def __init__(self, mode):
        self._title_pattern = '#\+([A-Z]+): ([/0-9a-zA-Z ]+)'
        self._task_pattern = '(\*+)([\w\s\dàé]+)(:[\w\s\d]+:\s)*(#[0-9]+)*'
        self._title_pattern = re.compile(self._title_pattern, re.UNICODE)
        self._task_pattern = re.compile(self._task_pattern, re.UNICODE)
        self._mode = mode

    def start(self, orgfile):
        #assert orgfile is FileType

        if (self._mode == "parser"):
            self._in = orgfile
            self._text = self.get_parse_text()
        else:
            self._out = orgfile
            self.write_parse_text()

    def get_parse_text(self):
        text = path(self._in).bytes()
        
        titles =  self._title_pattern.findall(text)

        if titles:
            for title in titles:
                print "{0} => {1}".format(title[0], title[1])

        tasks = self._task_pattern.findall(text)
        if tasks:
            for task in tasks:
                print "{0} => {1}".format(task[0], task[1])

    def write_parse_text():
        print self._mode
