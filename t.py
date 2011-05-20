##    Copyright (C) 2011 Oleg Kertanov <okertanov@gmail.com>
##    All rights reserved.

import os
import sys
import logging
import inspect
from GitLib import GitLib, GitLibDelegate, GitProjectItem, GitWorker

#
# GitLibTestDelegate class
#
class GitLibTestDelegate(GitLibDelegate) :
    def __init__(self, owner):
        super(GitLibTestDelegate, self).__init__(owner)

    def GetLoggingEnabled(self):
        return (True, logging.DEBUG, None, None)

    def GetTopDir(self):
        return "../"

    def Process(self, event, data):
        pass

    def OnProjects(self, items):
        pass

    def OnGitOutput(self):
        pass

def main():
    git = GitLib(GitLibTestDelegate(None))
    git.SetupGit({'topdir':'../'});
    git.Version()

    aList = git.Scan();
    map(lambda i: i.dump(), aList)

    git.Init();
    git.Clone();
    git.Status();
    git.Log();
    git.Diff();
    git.Config();

    worker = GitWorker()
    worker.enqueue(1).enqueue(2).enqueue(3)
    worker.enqueue(3).enqueue(2).enqueue(1)
    worker.execute()
    worker.block()
    worker.enqueue(10).enqueue(20).enqueue(30).execute()
    worker.enqueue('A').enqueue('B').enqueue('C').execute()
    worker.block()
    worker.enqueue(git.Init).enqueue(git.Status).enqueue(git.Log).execute()
    worker.block()

if __name__ == '__main__':
    main()

