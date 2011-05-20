##    Copyright (C) 2011 Oleg Kertanov <okertanov@gmail.com>
##    All rights reserved.

import os
import sys
import logging
import inspect
import GitLib

#
# GitLibTestDelegate class
#
class GitLibTestDelegate(GitLib.GitLibDelegate) :
    def __init__(self):
        super(GitLibTestDelegate, self).__init__()

    def GetLoggingEnabled(self):
        return (True, logging.DEBUG, None, None)

    def GetTopDir(self):
        return "~"

    def Process(self, event = None, data = None):
        pass

    def OnScanItem(self, item = None):
        pass

    def OnScanDone(self):
        pass

    def TestInit(self):
        self.git = GitLib.GitLib(self)
        self.git.SetupGit({'topdir':'../'});
        self.git.Version()

    def Test0(self):
        self.GetLoggingEnabled()
        self.GetTopDir()
        self.Process()
        self.OnScanItem()
        self.OnScanDone()

    def Test1(self):
        self.git.Scan();
        #map(lambda i: i.dump(), self.aList)

    def Test2(self):
        self.git.Init();
        self.git.Clone();
        self.git.Status();
        self.git.Log();
        self.git.Diff();
        self.git.Config();

    def Test3(self):
        self.worker = GitLib.GitWorker()
        self.worker.enqueue(1).enqueue(2).enqueue(3)
        self.worker.enqueue(3).enqueue(2).enqueue(1)
        self.worker.execute()
        self.worker.block()
        self.worker.enqueue(10).enqueue(20).enqueue(30).execute()
        self.worker.enqueue('A').enqueue('B').enqueue('C').execute()
        self.worker.block()
        self.worker.enqueue(self.git.Init).enqueue(self.git.Status).enqueue(self.git.Log).execute()
        self.worker.block()

    def RunTests(self):
        test.TestInit()
        test.Test0()
        test.Test1()
        test.Test2()
        test.Test3()

if __name__ == '__main__':
    test = GitLibTestDelegate()
    test.RunTests()

