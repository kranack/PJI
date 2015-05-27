# coding=utf-8

import Database
import re


class Task:

	def __init__(self):
		self._db = Database.Database('./database.db')
                self._title_pattern = '#\+([A-Z]+): ([/0-9a-zA-Z ]+)'
		self._task_keywords = ['DEADLINE', 'ASSIGN', 'FOLLOWERS', 'DEPENDS', 'SCHEDULED']
		self._task_status = ['DONE', 'NEXT']
		self._task_bloc_lines = '[^\n\r]+(?=\n|\z)'
		self._task_title = '(?<!@)([A-Z]+[éàa-z0-9 ]+)'
		self._task_date = '([A-Z]+)?:?\s+?([<0-9\/>]+)'
		self._task_user = '([A-Z]+)?:?\s+?(@\w+)'
		self._task_tag = ':(\w+):'
		self._task_ref = '#([0-9]+)'
		self._title_pattern = re.compile(self._title_pattern, re.UNICODE)
		self._task_bloc_lines = re.compile(self._task_bloc_lines, re.UNICODE)
		self._task_title = re.compile(self._task_title, re.UNICODE)
		self._task_date = re.compile(self._task_date, re.UNICODE)
		self._task_user = re.compile(self._task_user, re.UNICODE)
		self._task_tag = re.compile(self._task_tag, re.UNICODE)
		self._task_ref = re.compile(self._task_ref, re.UNICODE)
        
        
	def parse(self, bloc, title_id, task_id):
                self._title_id = title_id
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
				self._db.insert('Attach_Tag', [("tag_id", tag_id), ("task_id", next_id)])

		# User search

		users = self._task_user.findall(bloc.group(2))
                _users = ""
		if users:
			for user in users:
				if user[0]:
					if user[0] in self._task_keywords:
						if user[0] == 'ASSIGN':
							_users += "{0} affiliated to task #{1}\n".format(user[1], next_id)
							user_id = self._db.insert('Users', [("username", user[1]), ("email", ""), ("passwd", "")])
							self._db.insert('Assign_Tasks', [("user_id", user_id), ("task_id", next_id)])
						elif user[0] == 'FOLLOWERS':
							_users += "{0} follow task #{1}\n".format(user[1], next_id)
							user_id = self._db.insert('Users', [("username", user[1]), ("email", ""), ("passwd", "")])
							self._db.insert('Follow_Tasks', [("user_id", user_id), ("task_id", next_id)])
				else:
					_users += "{0} affiliated to task #{1}\n".format(user[1], next_id)
					user_id = self._db.insert('Users', [("username", user[1]), ("email", ""), ("passwd", "")])
					self._db.insert('Assign_Tasks', [("user_id", user_id), ("task_id", next_id)])
                
                self._task_id = next_id
		return task_id	
					
	def write(self):
		print "write file"
	
	def to_db(self):
		print "record to database"

        def titles_from_db(self):
            res = ""
            titles = self._db.select('Titles', [("raw_data")], "id = {0}".format(self._title_id))
            res += "{0}\n".format(titles[0][0])
            
            return res

        def from_db(self):
		res = ""
		tasks = self._db.select('Tasks', [("*")], "id = {0} AND raw_titles = {1}".format(self._task_id, self._title_id))
		for task in tasks:
                        tags_related = self._db.select('Attach_Tag', [("tag_id")], "task_id = {0}".format(task[0]))
                        tags = list()
                        for t in tags_related:
                                tag = self._db.select('Tags', [("*")], "id = {0}".format(t[0]))
                                tags.append(tag)
			res += "{0} ".format(task[6])
			if task[5] == 1:
				res += "DONE "
			elif task[5] == 2:
				res += "NEXT "
			res += u"{0}".format(task[1])
			if task[3] != "":
				res += " <{0}>".format(task[3])
                        for tag in tags:
                            res += " :{0}:".format(tag[0][1])
                        res += " #{0}".format(task[0])
			if task[2] != "":
				res += "\n\n{0}".format(task[2])
			res += "\n\n"
		
                return res

