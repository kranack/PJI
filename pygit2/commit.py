#!/usr/bin/python

import shutil, sys, pygit2


path_to_repository = pygit2.discover_repository('./pji')
repo = pygit2.Repository(path_to_repository)

last_commit = repo.revparse_single('HEAD')
#parents = last_commit.parents.id
parents = [repo.head.target]

#parents.append(last_commit.id)
print last_commit.id
print parents

author = pygit2.Signature('Damien Calesse', 'damien.calesse@gmail.com')
tree = repo.index.write_tree()

sha = repo.create_commit(
    'refs/heads/master',
    author, author, 'commit from pygit2',
    tree,
    parents
)

repo.index.write()
parent = [sha]

origin = repo.remotes["origin"]
origin.url = 'https://github.com/kranack/PJI.git'
origin.save()
origin.push([""], author, "")

#print "repository is bare :"
