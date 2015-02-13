#!/usr/bin/python

import shutil, sys, pygit2


shutil.rmtree('./pji')

#cred = pygit2.UserPass(username, password)
repo = pygit2.clone_repository('git://github.com/kranack/PJI.git', './pji')

print "repository is bare :" + str(repo.is_bare)
print repo.is_empty
