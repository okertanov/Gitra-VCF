##    Copyright (C) 2011 Oleg Kertanov <okertanov@gmail.com>
##    All rights reserved.

import os
import sys
import logging
import inspect
from GitLib import GitLib, GitLibDelegate, GitProjectItem

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

if __name__ == '__main__':
    main()

