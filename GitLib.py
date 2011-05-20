##    Copyright (C) 2011 Oleg Kertanov <okertanov@gmail.com>
##    All rights reserved.

import os
import sys
import socket
import logging
import inspect

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
    def __init__(self, owner):
        self.__owner = owner
        pass

    @property
    def owner(self):
        return self.__owner
    @owner.setter
    def owner(self, owner):
        self.__owner = owner

    def GetLoggingEnabled(self):
        raise NotImplementedError

    def GetTopDir(self):
        raise NotImplementedError

    def Process(self, event, data):
        raise NotImplementedError

    def OnProjects(self, items):
        raise NotImplementedError

    def OnGitOutput(self):
        raise NotImplementedError

#
# GitProjectItem class
#
class GitProjectItem(object) :
    def __init__(self, name = None, path = None):
        self.__name = name
        self.__path = path

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
        itemsList = []
        LOG.debug('Inside %s.%s', __name__, GitLib._fn_())
        top = self.topdir
        for dirpath, dirnames, filenames in os.walk(top, topdown=True):
            for name in dirnames:
                if DOTGITDIR == name:
                    fullgit  = os.path.abspath(os.path.join(dirpath, name))
                    fullpath = os.path.split(fullgit)[0]
                    projpath, projname = os.path.split(fullpath)
                    LOG.debug('Found git project: [%s] at %s', projname, projpath)
                    itemsList.append(GitProjectItem(projname, fullpath))
                    dirnames.remove(name)
        if hasattr(self.delegate, 'OnProjects'):
            self.delegate.OnProjects(itemsList)
        return itemsList

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

