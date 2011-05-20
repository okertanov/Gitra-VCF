##    Copyright (C) 2011 Oleg Kertanov <okertanov@gmail.com>
##    All rights reserved.

import os
import sys
import time
import types
import socket
import logging
import inspect
import Queue
from PyQt4 import QtCore, QtGui

GITLIBAPPNAME = 'Gitra'
GITLIBVERSION = '1.00'
GITLIBORGNAME = 'espectrale.com'
GITLIBORGDOMAIN = 'gitra.espectrale.com'
LOG = logging.getLogger(__name__)
DOTGITDIR = '.git'

#
# GitLibDelegate class
#
class GitLibDelegate(object) :
    def __init__(self):
        pass

    def GetLoggingEnabled(self):
        raise NotImplementedError

    def GetTopDir(self):
        raise NotImplementedError

    def Process(self, event = None, data = None):
        raise NotImplementedError

    def OnScanItem(self, item = None):
        raise NotImplementedError

    def OnScanDone(self):
        raise NotImplementedError

#
# GitProjectItem class
#
class GitProjectItem(object) :
    class ProjStatus:
        Unknown, Clean, Changed, Staged, Conflicted = range(5)

    class FileStatus:
        Unknown, Unmodified, Modified, Added, Deleted, Renamed, Copied, Unmerged = range(8)

    def __init__(self, name = None, path = None):
        self.__name   = name
        self.__path   = path
        self.__status = GitProjectItem.ProjStatus.Unknown

    def __str__(self):
        return "[" + self.__name + "] : " + self.__path

    def dump(self):
        LOG.debug(self)

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = name
    @property
    def path(self):
        return self.__path
    @path.setter
    def path(self, path):
        self.__path = path
    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, status):
        self.__status = status

#
# GitWorker class
#
class GitWorker(QtCore.QThread) :
    __pyqtSignals__ = ("sig_ready", "sig_inprogress")

    def __init__(self, parent = None):
        super(GitWorker, self).__init__(parent)
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        self.quit = False
        self.condition = QtCore.QWaitCondition()
        self.mutex = QtCore.QMutex()
        self.queue = Queue.Queue()
        self.start(QtCore.QThread.LowPriority)
        pass

    def __del__(self):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        self.mutex.lock()
        self.quit = True
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait()

    def run(self):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        while not self.quit:
            self.mutex.lock()
            self.condition.wait(self.mutex)
            while (not self.queue.empty() and not self.quit):
                f = self.queue.get()
                LOG.debug('GitWorker: Running for item... %s', f)
                if (type(f) == types.MethodType or
                    type(f) == types.BuiltinMethodType or
                    type(f) == types.LambdaType):
                    f()
                self.queue.task_done()
            self.mutex.unlock()
            pass

    def sleep(self, sec):
        time.sleep(sec)

    def enqueue(self, command):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        self.mutex.lock()
        self.queue.put(command)
        self.mutex.unlock()
        return self

    def execute(self):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        locker = QtCore.QMutexLocker(self.mutex)
        self.condition.wakeOne()
        return self

    def block(self):
        if not self.queue.empty():
            self.queue.join()
        return self

#
# GitLib class
#
class GitLib() :
    def __init__(self, delegate):
        self.delegate = delegate

        if hasattr(self.delegate, 'GetLoggingEnabled'):
            logenabled, loglevel, logfile, loghandler = self.delegate.GetLoggingEnabled()
            if logenabled:
                self.SetupLogging(loglevel, logfile, loghandler)
        if hasattr(self.delegate, 'GetTopDir'):
            self.topdir = self.delegate.GetTopDir()
        else:
            self.topdir = os.path.expanduser('~')
        pass

    @staticmethod
    def _fn_():
        return inspect.stack()[1][3]

    @staticmethod
    def Version():
        return GITLIBVERSION

    @staticmethod
    def Log(s):
        LOG.debug(s)

    def SetupGit(self, parameters = {}):
        if parameters.has_key('topdir'):
            self.topdir = parameters['topdir']
        pass

    def SetupLogging(self, loglevel = logging.DEBUG, logfile = None, loghandler = None):
        self.logfile = logfile
        self.loglevel = loglevel
        self.logformat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

        if self.logfile is None:
            logging.basicConfig(level=self.loglevel, format=self.logformat)
        else:
            logfilename = os.path.normpath(self.logfile)
            logging.basicConfig(level=self.loglevel, format=self.logformat, filename=logfilename, filemode='a')
        if loghandler != None:
            LOG.debug('Adding Log handler... %s', loghandler)
            LOG.addHandler(loghandler)
        LOG.info('Initializing %s, rev %s from %s using verbosity %s as PID %d', __name__, GitLib.Version(), os.path.split(__file__)[1], self.loglevel, os.getpid())
        pass

    def Scan(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        top = self.topdir
        for dirpath, dirnames, filenames in os.walk(top, topdown=True):
            for name in dirnames:
                if DOTGITDIR == name:
                    fullgit  = os.path.abspath(os.path.join(dirpath, name))
                    fullpath = os.path.split(fullgit)[0]
                    projpath, projname = os.path.split(fullpath)
                    LOG.debug('Found git project: [%s] at %s', projname, projpath)
                    item = GitProjectItem(projname, fullpath)
                    if hasattr(self.delegate, 'OnScanItem'):
                        self.delegate.OnScanItem(item)
                    dirnames.remove(name)
        if hasattr(self.delegate, 'OnScanDone'):
                        self.delegate.OnScanDone()
        pass

    def Init(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

    def Clone(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

    def Status(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

    def Log(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

    def Diff(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

    def Config(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

    def Pull(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

    def Fetch(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

    def Commit(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

    def Push(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

    def Branch(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

    def Tag(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

    def Merge(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

    def Rebase(self, actctx = None):
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        pass

