#!/usr/bin/python

import shutil, sys, pygit2


path_to_repository = pygit2.discover_repository('./pji')
repo = pygit2.Repository(path_to_repository)

last_commit = repo.revparse_single('HEAD')
parents = last_commit.parents

master_ref = repo.lookup_reference('refs/heads/master')
master_ref.set_target(last_commit.id)
repo.head.set_target(last_commit.id)

print repo

#last_commit = repo.revparse_single('HEAD')
#parents = last_commit.parents

parents.append(last_commit.id)
print last_commit.id
print parents
print repo.status()
repo.index.write_tree()
repo.index.write()
